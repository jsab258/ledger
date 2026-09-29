using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.DevTools
{
    /// A MODEL CALL THROUGH CLAUDE CODE, ON JAFAR'S SUBSCRIPTION (Jafar, 29
    /// September: "nothing in development calls the Anthropic API directly";
    /// model work runs through Claude Code's non-interactive mode, which uses
    /// the session's own login). Each request is one `claude -p` run: the
    /// request's system prompt as its whole system prompt, no tools, no
    /// settings, skills, MCP servers or project files, nothing kept, the
    /// request's model; the reply's text and token counts read from its JSON.
    ///
    /// NEVER A KEY: ANTHROPIC_API_KEY is taken out of the child's environment
    /// and `--bare`, which signs in only with a key, is never used, so a key
    /// left in the environment can never be billed; the login is the one
    /// `claude auth status` shows. The dev tools use this and nothing else
    /// (the game's live talk, on its own capped key, is the only exception).
    ///
    /// What differs from the game's own call: an earlier conversation is sent
    /// as one message with the turns written out (the non-interactive mode
    /// takes one prompt), and Claude Code adds a few hundred tokens of its
    /// own to each request.
    public sealed class ClaudeCodeClient : ILlmClient, IDisposable
    {
        /// Where Claude Code is: LEDGER_CLAUDE, else the one this session
        /// runs (CLAUDE_CODE_EXECPATH), else claude.exe or claude.cmd on PATH.
        public string Executable = Find();
        /// The longest one call may take before it is given up.
        public TimeSpan Timeout = TimeSpan.FromMinutes(3);
        /// Claude Code in the same folder as nothing: no CLAUDE.md, no project.
        readonly string _workDir;

        public ClaudeCodeClient()
        {
            _workDir = Path.Combine(Path.GetTempPath(), "ledger-claude-code");
            Directory.CreateDirectory(_workDir);
        }

        public void Dispose() { }

        static string Find()
        {
            foreach (var v in new[] { "LEDGER_CLAUDE", "CLAUDE_CODE_EXECPATH" })
            {
                var p = Environment.GetEnvironmentVariable(v);
                if (!string.IsNullOrEmpty(p) && File.Exists(p)) return p;
            }
            foreach (var dir in (Environment.GetEnvironmentVariable("PATH") ?? "").Split(Path.PathSeparator))
                foreach (var name in new[] { "claude.exe", "claude.cmd", "claude" })
                {
                    try
                    {
                        var p = Path.Combine(dir.Trim('"'), name);
                        if (File.Exists(p)) return p;
                    }
                    catch (ArgumentException) { }
                }
            return "claude";
        }

        /// The request as one prompt: its last message, and any earlier turns
        /// written out before it.
        public static string PromptFor(LlmRequest request)
        {
            var msgs = request.Messages ?? new List<LlmMessage>();
            if (msgs.Count == 0) return "";
            if (msgs.Count == 1) return msgs[0].Content ?? "";
            var sb = new StringBuilder("The conversation so far, oldest first:\n\n");
            for (int i = 0; i < msgs.Count - 1; i++)
                sb.Append(msgs[i].Role == "assistant" ? "You: " : "Them: ").Append(msgs[i].Content).Append("\n\n");
            sb.Append("Now they say:\n\n").Append(msgs[msgs.Count - 1].Content);
            return sb.ToString();
        }

        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            var psi = new ProcessStartInfo
            {
                FileName = Executable,
                WorkingDirectory = _workDir,
                UseShellExecute = false,
                RedirectStandardInput = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8,
                CreateNoWindow = true,
            };
            if (Executable.EndsWith(".cmd", StringComparison.OrdinalIgnoreCase))
            {
                psi.FileName = Environment.GetEnvironmentVariable("ComSpec") ?? "cmd.exe";
                psi.ArgumentList.Add("/c");
                psi.ArgumentList.Add(Executable);
            }
            foreach (var a in new[] { "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
                                      "--setting-sources", "", "--disable-slash-commands", "--strict-mcp-config" })
                psi.ArgumentList.Add(a);
            if (!string.IsNullOrEmpty(request.Model)) { psi.ArgumentList.Add("--model"); psi.ArgumentList.Add(request.Model); }
            psi.ArgumentList.Add("--system-prompt");
            psi.ArgumentList.Add(string.IsNullOrEmpty(request.System) ? "You are a helpful assistant." : request.System);
            psi.Environment.Remove("ANTHROPIC_API_KEY");
            psi.Environment.Remove("ANTHROPIC_AUTH_TOKEN");
            psi.Environment["MAX_THINKING_TOKENS"] = "0";

            using var p = new Process { StartInfo = psi };
            p.Start();
            await p.StandardInput.WriteAsync(PromptFor(request));
            p.StandardInput.Close();
            var outTask = p.StandardOutput.ReadToEndAsync();
            var errTask = p.StandardError.ReadToEndAsync();
            using var limit = CancellationTokenSource.CreateLinkedTokenSource(ct);
            limit.CancelAfter(Timeout);
            try { await p.WaitForExitAsync(limit.Token); }
            catch (OperationCanceledException)
            {
                try { p.Kill(true); } catch (Exception) { }
                ct.ThrowIfCancellationRequested();
                throw new TimeoutException("claude -p took longer than " + Timeout);
            }
            string stdout = await outTask, stderr = await errTask;
            JsonDocument doc;
            try { doc = JsonDocument.Parse(stdout); }
            catch (JsonException) { throw new InvalidOperationException("claude -p gave no JSON: " + Trim(stdout + " " + stderr)); }
            using (doc)
            {
                var r = doc.RootElement;
                if (r.TryGetProperty("is_error", out var e) && e.ValueKind == JsonValueKind.True)
                    throw new InvalidOperationException("claude -p failed: " + Trim(r.TryGetProperty("result", out var er) ? er.ToString() : stdout));
                var resp = new LlmResponse { Text = r.TryGetProperty("result", out var t) ? t.GetString() ?? "" : "", StopReason = "end_turn", Model = request.Model ?? "" };
                if (r.TryGetProperty("usage", out var u))
                {
                    int Int(string k) => u.TryGetProperty(k, out var x) && x.ValueKind == JsonValueKind.Number ? x.GetInt32() : 0;
                    resp.InputTokens = Int("input_tokens") + Int("cache_creation_input_tokens") + Int("cache_read_input_tokens");
                    resp.OutputTokens = Int("output_tokens");
                }
                if (r.TryGetProperty("modelUsage", out var mu) && mu.ValueKind == JsonValueKind.Object)
                    foreach (var m in mu.EnumerateObject()) { resp.Model = m.Name; break; }
                return resp;
            }
        }

        static string Trim(string s) => s == null ? "" : s.Length > 400 ? s.Substring(0, 400) + "..." : s;
    }
}
