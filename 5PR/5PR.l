%option noyywrap yylineno
%{
    #include <stdio.h>
    #include <string.h>
    int ch;
%}
literal (true|false|null)
string ((\"[^\"]*\")|(\'[^\']*\'))
digit [0-9]
number ([-+]?({digit}*\.{digit}+|{digit}+\.|{digit}+)([eE][-+]?{digit}+)?[flFL]?)
ws [ \t\n]+
%%
\{				{printf("(BEGIN_OBJECT, %s)\n", yytext); ch += yyleng;}
\}				{printf("(END_OBJECT, %s)\n", yytext); ch += yyleng;}
\[				{printf("(BEGIN_ARRAY, %s)\n", yytext); ch += yyleng;}
\]				{printf("(END_ARRAY, %s)\n", yytext); ch += yyleng;}
,				{printf("(COMMA, %s)\n", yytext); ch += yyleng;}
:				{printf("(COLON, %s)\n", yytext); ch += yyleng;}

{literal}			{printf("(LITERAL: %s)\n", yytext); ch += yyleng;}
{string}			{printf("(STRING, %s)\n", yytext); ch += yyleng;}
{number}			{printf("(NUMBER, %s)\n", yytext); ch += yyleng;}
{ws}				{ch += yyleng;}
[^a-zA-Z0-9 \.\"\'\+\-\n\t]	{printf("(UNKNOWN CHARACTER, %s)\n", yytext); ch += yyleng;}
%%
int main(int argc, char **argv) {
    if(argc < 2) {
        printf("\nNot enough arguments. Please specify filename.\n");
        return -1;
    }

    if((yyin = fopen(argv[1], "r")) == NULL) {
        printf("\nCannot open file %s.\n", argv[1]);
        return -1;
    }
    
    ch = 1;
    yylineno = 1;
    printf("Tokenlist:\n");
    yylex();
    fclose(yyin);
    return 0;
}
