%option noyywrap
%{
#include<stdio.h>
int Upper=0;
int Lower=0;
%}
%%
[A-Z] {printf("Uppercase\t");Upper++;}
[a-z] {printf("Lowercase\t");Lower++;}
%%
main()
{
printf("Enter a string\n");
yylex();
printf("Uppercase=%d and Lowercase=%d",Upper,Lower);
}