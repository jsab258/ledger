Questions written 28 October 2026 before reading anything (research method, Jafar 13 Oct).

1. What does Unreal 5.8 itself ship for asset validation? Data Validation plugin, EditorValidatorSubsystem, UEditorValidatorBase (C++ and Python subclasses), the validators that ship in Engine/Plugins/Editor/DataValidation and Engine/Source/Editor, the DataValidation commandlet (exact command line, output, headless on one folder), Asset Audit, "Validate Assets", and any built-in rule for triangles, texture size, names, LODs, collision, Nanite, missing references.
2. What do studios and Epic's samples check automatically (naming prefixes, budgets per asset class)? What do Study 13 and Study 12 give for Mafia / KCD2 conventions and budgets?
3. How do pieces reach a gate today, and which faults did reviewers catch that a machine check would have caught? Gate rounds and reviews per piece over the last two weeks (the "before"), with the counting rule.
4. Which validators to write, each rule with threshold and source, where it runs, how the report is read, how "after" is measured; first use on the next piece (jacket or office); hours.
