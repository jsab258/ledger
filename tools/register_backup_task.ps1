# THE NIGHTLY BACKUP'S SCHEDULE (advisor 197, his pick of 17 Nov 2026 12:58): tools/backup-to-dropbox.py --log
# every day at 05:00, after retention (03:30) and the morning pictures (04:15), whether or not there was a commit.
# The post-commit hook stays as a second chance. The app's safety check refused this registration to the session
# (17 Nov 13:2x), so it runs at his word at the PC. Re-running replaces the task with the same settings.
$action = New-ScheduledTaskAction -Execute 'C:\Users\Jafar\miniconda3\pythonw.exe' `
    -Argument '"C:\Users\Jafar\ledger-local\tools\backup-to-dropbox.py" --log' -WorkingDirectory 'C:\Users\Jafar\ledger-local'
$trigger = New-ScheduledTaskTrigger -Daily -At 05:00
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 3)
Register-ScheduledTask -TaskName 'LEDGER backup' -Action $action -Trigger $trigger -Settings $settings -Force `
    -Description 'Nightly copy of the lasting shelf to his Dropbox (advisor 197); never deletes or overwrites.' |
    Select-Object TaskName, State
