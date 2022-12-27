# Winterfest Present Opener

This program allows you to automatically open all currently available Winterfest presents.

---
### Changelog:
What's new in the 1.0.1 update:
- Made the program open presents significantly faster using threading.
- Tweaked the program's code a little bit.
---

### How to use it?

- If you didn't do it yet, install the python requests module using the pip install requests console command.

- After starting the WinterfestPresentOpener.py for the first time or after you delete the auth.json file, you will be asked if you are logged into your Epic account in your browser. If yes, type 1. If not, type 2.

- After you'll press ENTER, an Epic Games website will open. From there, login if you are not already logged into your Epic account.

- Then a page should open with content similar to this:

```json
{"redirectUrl":"https://localhost/launcher/authorized?code=930884289b5852842271e9027376a527","authorizationCode":"930884289b5852842271e9027376a527","sid":null}
```

- Copy the code (e.g. 930884289b5852842271e9027376a527), paste it into the program and press enter.

- If all went well, the program will say it has generated the auth.json file successfully.

- Now the program will open all available Winterfest presents.
---

### Found a bug?
Feel free to [open an issue](https://github.com/PRO100KatYT/WinterfestPresentOpener/issues/new "Click here if you want to open an issue.") if you encounter any bugs or just have a question.
