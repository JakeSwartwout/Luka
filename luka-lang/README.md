# luka-lang Overview

This extension serves to be a syntax highlighter is VS Code for the Luka programming language.

## How to Use

To enable this extension, place the entire `luka-lang` folder into your `<user name>/.vscode/extensions` folder, then reload VS Code.

For development, to view what each token is classified as, type <kbd>CTRL</kbd> + <kbd>SHIFT</kbd> + <kbd>P</kbd>. Then, choose the option for <kbd>Developer: Inspect Editor Tokens and Scopes</kbd>. I included a python file with some examples of different types of text to use this on, and comments of what they ended up being.

The actual syntax is defined in the syntaxes/luka.tmLanguage.json file. This recursively looks for the different types to label them, using regex to look for an exact match, or the correct start and end tokens. It then references these standard naming conventions:
https://macromates.com/manual/en/language_grammars#naming_conventions  
and then whatever theme the user is using should be able to read those tags and colorize as they have chosen.

## Known Issues

- I've never made an extension or syntax highlighter before.
- I didn't put much effort into this extension

## Release Notes

8/16/2021 Release: Adding the framework for the base extensions, plus some test files.
