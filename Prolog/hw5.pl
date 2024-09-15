parent(pam, bob).		% Pam is a parent of Bob
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(bob, jim).	% pam is a female
female(pam).	% Tom is a male
male(tom).
male(bob).
female(liz).
female(ann).
female(pat).
male(jim).

mother(X, Y) :-	% X is the mother of Y if
	parent(X, Y),	% X is a parent of Y and
	female(X).	% X is female

predecessor(X, Y) :-	% Rule pr1:	X is a predecessor of Y if
	parent(X, Y).	%		X is a parent of Y

predecessor(X,Y) :-	% Rule pr2:	X is a predecessor of Y if
	parent(X, Z),	%		X is a parent of Z and
	predecessor(Z, Y).	%		Z is a predecessor of Y

happy(X):- parent(X, Y).
hasTwoChildren(X):- parent(X, Z), sister(Z, Y).
grandChild(X, Y):- parent(Z, X), parent(Y, Z).
aunt(X, Y):- parent(X, Z), sister(Z, Y).
