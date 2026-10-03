using System;
using System.Threading;
using System.Threading.Tasks;

namespace Ledger.Core
{
    /// The day's budget is spent: no more calls on this client.
    public class BudgetSpentException : Exception
    {
        public BudgetSpentException(string message) : base(message) { }
    }

    /// THE KEY'S CAP, ENFORCED IN CODE (Jafar, 30 September: "a run labelled
    /// about a dollar cost $14.50; every run checks its estimated cost first and
    /// stops at the day's dollar"). Wraps the client a paid run talks through.
    /// Before each call it reserves the call's worst case: its input at about
    /// four characters a token, a tenth more for safety, and every output token
    /// it may use, at the rate card, the dearest rate for a model the card does
    /// not know. A call that would take the run past its limit is refused, never
    /// sent. After the call, the reserve settles to the tokens the reply says it
    /// used. A call that fails keeps its reserve, since a request that reached
    /// the service may be billed.
    public sealed class BudgetedClient : IStreamingLlmClient, IDisposable
    {
        readonly ILlmClient _inner;
        /// The client this cap wraps: what the run really talks to (the claim check asks, P3).
        public ILlmClient Inner => _inner;
        readonly object _gate = new object();
        double _spent;

        public double LimitUsd { get; }
        /// Spent and reserved so far, US dollars.
        public double SpentUsd { get { lock (_gate) return _spent; } }
        /// How many calls were refused for the budget.
        public int Refused { get; private set; }

        /// Told the spend after every reserve and settlement, outside the lock, so a
        /// friends' evening can keep it across the game's restarts (P5, 3 October).
        public Action<double> OnSpent { get; set; }

        /// spentBefore: what this budget's evening has already spent (P5: his friends'
        /// five dollars is an evening's, never a game start's).
        public BudgetedClient(ILlmClient inner, double limitUsd, double spentBefore = 0)
        {
            _inner = inner ?? throw new ArgumentNullException(nameof(inner));
            LimitUsd = double.IsNaN(limitUsd) || limitUsd < 0 ? 0 : limitUsd;
            _spent = double.IsNaN(spentBefore) || spentBefore < 0 ? 0 : spentBefore;
        }

        /// The most a request can cost: its input at four characters a token and
        /// a tenth more, and all of its output allowance.
        public static double WorstCaseUsd(LlmRequest r)
        {
            if (r == null) return 0;
            long chars = (r.System ?? "").Length;
            foreach (var m in r.Messages) chars += (m.Content ?? "").Length;
            double inTokens = chars / 4.0 * 1.1 + 50;
            var rate = RateOf(r.Model);
            return inTokens / 1_000_000.0 * rate.inPerM + Math.Max(0, r.MaxTokens) / 1_000_000.0 * rate.outPerM;
        }

        static (double inPerM, double outPerM) RateOf(string model)
        {
            if (model != null && Models.Cost.TryGetValue(model, out var known)) return known;
            double inMax = 0, outMax = 0;
            foreach (var r in Models.Cost.Values) { inMax = Math.Max(inMax, r.inPerM); outMax = Math.Max(outMax, r.outPerM); }
            return (inMax, outMax);
        }

        static double ActualUsd(string model, LlmResponse resp)
        {
            var rate = RateOf(model);
            return resp.InputTokens / 1_000_000.0 * rate.inPerM + resp.OutputTokens / 1_000_000.0 * rate.outPerM;
        }

        double Reserve(LlmRequest r)
        {
            double worst = WorstCaseUsd(r);
            lock (_gate)
            {
                if (_spent + worst > LimitUsd)
                {
                    Refused++;
                    throw new BudgetSpentException($"the budget of US${LimitUsd:0.00} is spent (US${_spent:0.0000} so far; this call could cost US${worst:0.0000})");
                }
                _spent += worst;
            }
            Report();
            return worst;
        }

        void Report()
        {
            var tell = OnSpent;
            if (tell != null) tell(SpentUsd);
        }

        void Settle(double reserved, LlmRequest r, LlmResponse resp)
        {
            if (resp == null) return;
            double actual = ActualUsd(resp.Model ?? r.Model, resp);
            lock (_gate) _spent += actual - reserved;
            Report();
        }

        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            double reserved = Reserve(request);
            var resp = await _inner.CompleteAsync(request, ct).ConfigureAwait(false);
            Settle(reserved, request, resp);
            return resp;
        }

        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default)
        {
            double reserved = Reserve(request);
            LlmResponse resp;
            if (_inner is IStreamingLlmClient streaming) resp = await streaming.StreamAsync(request, onText, ct).ConfigureAwait(false);
            else
            {
                resp = await _inner.CompleteAsync(request, ct).ConfigureAwait(false);
                onText?.Invoke(resp?.Text ?? "");
            }
            Settle(reserved, request, resp);
            return resp;
        }

        public void Dispose() => (_inner as IDisposable)?.Dispose();
    }
}
