rodzic(marek, jan). % X jest rodzicem Y
rodzic(anna, jan).
rodzic(marek, adam).
%rodzic(anna, adam).
rodzic(czarek, marek).
rodzic(czarek, janusz).
rodzic(janusz, brajan).

rodzic(maria, beata).
rodzic(beata, anna).

mezczyzna(marek).
mezczyzna(jan).
mezczyzna(adam).
kobieta(X) :-
	 \+ mezczyzna(X).

% X jest ojcem Y
ojciec(X, Y) :-
	rodzic(X, Y),
	mezczyzna(X).

% X jest matką Y
matka(X, Y) :-
	rodzic(X, Y),
	kobieta(X).

% X jest córką Y
corka(X, Y) :-
	rodzic(Y, X),
	kobieta(Y).

% X jest rodzonym bratem Y
brat_rodzony(X, Y) :-
	mezczyzna(X),
	ojciec(O, X),
	ojciec(O, Y),
	matka(M, X),
	matka(M, Y).

% X jest przyrodnim bratem Y
brat_przyrodni(X, Y) :-
	mezczyzna(X),
	once(
		(ojciec(O, X), ojciec(O, Y));
		(matka(M, X), matka(M, Y))
    ).

% X jest kuzynem Y
kuzyn(X, Y) :-
	rodzic(A, X),
	rodzic(B, Y),
	rodzic(C, A),
	rodzic(C, B).
% X jest dziadkiem od strony ojca dla Y
dziadek_od_strony_ojca(X, Y) :-
	ojciec(X, Z),
	ojciec(Z, Y).

% X jest dziadkiem od strony matki dla Y
dziadek_od_strony_matki(X, Y) :-
	ojciec(X, Z),
	matka(Z, Y).

% X jest dziadkiem Y
dziadek(X, Y) :-
	mezczyzna(X),
	rodzic(X, Z),
	rodzic(Z, Y).

% X jest babcią Y
babcia(X, Y) :-
	kobieta(X),
	rodzic(X, Z),
	rodzic(Z, Y).

% Y jest wnuczką X
wnuczka(Y, X) :-
	kobieta(Y),
	rodzic(Z, Y),
	rodzic(X, Z).

% X jest przodkiem Y do drugiego pokolenia wstecz
przodek_do2pokolenia_wstecz(X, Y) :-
	rodzic(X, Z),
	rodzic(Z, Y).

% X jest przodkiem Y do trzeciego pokolenia wstecz
przodek_do3pokolenia_wstecz(X, Y) :-
	rodzic(X, A),
	rodzic(A, Z),
	rodzic(Z, Y).
