using System;
using System.IO;
using UnityEngine;

namespace Ledger.Game
{
    /// THE LIVE-TALK KEY, AND ONLY IT (Jafar, 29 September: nothing in
    /// development calls the Anthropic API; the one exception is the
    /// characters talking live while he plays, on LEDGER's own key with a hard
    /// monthly cap, which no automated tool or workflow may use). The key is
    /// read from one file, %LOCALAPPDATA%\LEDGER\live-talk-key.txt, the same
    /// one the Unreal game reads, and never from the environment (a key set
    /// there for anything else must not reach the talk) nor in a batch run
    /// nobody is at. It never ships inside the build or the repo. Until 29
    /// September this read ANTHROPIC_API_KEY first and then secrets.json, which
    /// held another project's key.
    public static class Secrets
    {
        static string FilePath => Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "LEDGER", "live-talk-key.txt");

        public static string LoadAnthropicKey()
        {
            if (Application.isBatchMode) return null;
            try
            {
                if (File.Exists(FilePath))
                {
                    var key = File.ReadAllText(FilePath).Trim();
                    if (!string.IsNullOrEmpty(key)) return key;
                }
            }
            catch (Exception e)
            {
                Debug.LogWarning($"Secrets: could not read the live-talk key file: {e.Message}");
            }
            return null;
        }

        /// The in-game prompt's key, kept in the same one file.
        public static void SaveAnthropicKey(string key)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(FilePath));
            File.WriteAllText(FilePath, key.Trim());
        }
    }
}
