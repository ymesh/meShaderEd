#ifndef RAYSPHERE_H
#define RAYSPHERE_H
/************************************************************************
 * raysphere.h - intersect a ray with a sphere (this is a useful
 *               solution to subproblems that crop up frequently)
 *
 * Entropy and BMRT are:
 * (c) Copyright 2001 Exluna, Inc.  Portions (c) 1990-2000 Larry Gritz.
 * All rights reserved.
 *
 * $Revision: 1.4 $    $Date: 2001/06/15 23:45:26 $
 *
 ************************************************************************/

/* raysphere - calculate the intersection of ray (E,I) with a sphere
 * centered at the origin and with radius r.  We return the number of
 * intersections found (0, 1, or 2), and place the distances to the
 * intersections in t0, t1 (always with t0 <= t1).  Ignore any hits
 * closer than eps.
 */
float
raysphere(  point E; 
            vector I;   /* Origin and unit direction of the ray */
            uniform float r; /* radius of sphere */
              float eps;           /* epsilon - ignore closer hits */
              output float t0, t1; /* distances to intersection */
         )
{
    /* Set up a quadratic equation -- note that a==1 if I is normalized */
    float b = 2 * ((vector E) . I);
    float c = ((vector E) . (vector E)) - r*r;
    float discrim = b*b - 4*c;
    float solutions;
    if (discrim > 0) 
    {           /* Two solutions */
        discrim = sqrt(discrim);
        t0 = (-discrim - b) / 2;
        if (t0 > eps) {
            t1 = (discrim - b) / 2;
            solutions = 2;
        } else {
            t0 = (discrim - b) / 2;
            solutions = (t0 > eps) ? 1 : 0;
        }
    } 
    else if (discrim == 0) 
    {  /* One solution on the edge! */
        t0 = -b/2;
        solutions = (t0 > eps) ? 1 : 0;
    } 
    else 
    { /* Imaginary solution -> no intersection */
        solutions = 0;
    }
    return solutions;
}

#endif
