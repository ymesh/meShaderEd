#ifndef GRAYSCALE_H
#define GRAYSCALE_H 1



/*
===============================================================================
																Grayscale functions
===============================================================================
			Author: DRL

Converts given color to grayscale float value.
There are 3 types of grayscale functions:
	grayscale_709 (preferrable): Rec. 709 (0.2126 R, 0.7152 G, 0.0722)
	grayscale_601: Rec. 601 (0.299 R, 0.587 G, 0.114 B)
	grayscale_avg: Simple average between RGB colors.
	grayscale_custom: Lets specify custom color coefficients. Arguments are:
		input color,
		R coefficient,
		G coefficient,
		B coefficient
*/

// ---------->         709         <----------
float grayscale_709 (color Clr) {
	return (
		comp(Clr, 0) * 0.2126
		+ comp(Clr, 1) * 0.7152
		+ comp(Clr, 2) * 0.0722
	);
}
uniform float grayscaleUni_709 (uniform color Clr) {
	return (
		comp(Clr, 0) * 0.2126
		+ comp(Clr, 1) * 0.7152
		+ comp(Clr, 2) * 0.0722
	);
}

// ---------->         601         <----------
float grayscale_601 (color Clr) {
	return (
		comp(Clr, 0) * 0.299
		+ comp(Clr, 1) * 0.587
		+ comp(Clr, 2) * 0.114
	);
}
uniform float grayscaleUni_601 (uniform color Clr) {
	return (
		comp(Clr, 0) * 0.299
		+ comp(Clr, 1) * 0.587
		+ comp(Clr, 2) * 0.114
	);
}

// ---------->         Average         <----------
float grayscale_avg (color Clr) {
	return (
		(
			comp(Clr, 0)
			+ comp(Clr, 1)
			+ comp(Clr, 2)
		)
		/ 3
	);
}
uniform float grayscaleUni_avg (uniform color Clr) {
	return (
		(
			comp(Clr, 0)
			+ comp(Clr, 1)
			+ comp(Clr, 2)
		)
		/ 3
	);
}

// ---------->         Custom         <----------
float grayscale_custom (
	color Clr;
	float
		Kr,
		Kg,
		Kb
) {
	return (
		comp(Clr, 0) * Kr
		+ comp(Clr, 1) * Kg
		+ comp(Clr, 2) * Kb
	);
}
uniform float grayscaleUni_custom (
	uniform color Clr;
	uniform float
		Kr,
		Kg,
		Kb;
) {
	return (
		comp(Clr, 0) * Kr
		+ comp(Clr, 1) * Kg
		+ comp(Clr, 2) * Kb
	);
}


#endif /* GRAYSCALE_H */