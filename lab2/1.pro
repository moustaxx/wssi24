lubi(jan, pawel).
lubi(pawel, krzysztof).
lubi(pawel, jan).
lubi(jan, bartek).
lubi(bartek, jan).

lubi(bartek, asia).
lubi(asia, bartek).
lubi(asia, pawel).

przyjazn(X, Y) :-
    lubi(X, Y),
    lubi(Y, X).

niby_przyjazn(X, Y) :-
    lubi(X, Y);
    lubi(Y, X).

nieprzyjazn(X, Y) :-
    \+niby_przyjazn(X, Y).

mezczyzna(jan).
mezczyzna(pawel).
mezczyzna(krzysztof).
mezczyzna(bartek).
kobieta(asia).
kobieta(basia).
kobieta(kasia).

loves(X, Y) :-
    przyjazn(X, Y),
    (mezczyzna(X), kobieta(Y)) ; (kobieta(X), mezczyzna(Y)).

true_love(X, Y) :-
    loves(X, Y),
    \+ (loves(X, Z), Z \= Y, loves(Z, X)),
    \+ (loves(Y, W), W \= X, loves(W, Y)).
