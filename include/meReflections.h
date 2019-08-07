/************************************************************************
 * reflections.h - Functions which compute reflected light by either
 *                 ray tracing or environment mapping.
 *
 * Entropy / BMRT are:
 * (c) Copyright 1990-2001 Exluna, Inc. and Larry Gritz. All rights reserved.
 *
 * $Revision: 1.13 $    $Date: 2001/09/26 18:22:52 $
 *
 ************************************************************************/


#ifndef REFLECTIONS_H
#define REFLECTIONS_H

#include "filterwidth.h"
#include "raysphere.h"


#define ENVPARAMS \
        envname, envspace, envrad, samples

#define DECLARE_ENVPARAMS                           \
        string envname, envspace;                   \
        uniform float envrad, samples

#define DECLARE_DEFAULTED_ENVPARAMS                                 \
        string envname = "", envspace = "current";                  \
        uniform float envrad = 0, samples = 1



/* Environment() - A does-all replacement for environment() lookups 
 * (including parallax, if desired), flat reflection maps, and even
 * ray tracing (if supported).
 *
 * Inputs are:
 *    envname - filename of environment map
 *    envspace - name of space environment map was made in
 *    envrad - approximate supposed radius of environment sphere
 *    P, R - position and direction of traced ray
 *    blur - amount of additional blur to add to environment map
 * Outputs are:
 *    return value - the color of incoming environment light
 *
 * In ordinary circumstances, we just do environment mapping, assuming
 * that the environment map was formed in the named coordinate system
 * given by envspace.  If envrad != 0, we do "fake ray tracing" against
 * a sphere of that radius, in order to simulate parallax.
 * 
 * If flat reflection mapping is desired, envspace must be "NDC" and
 * envname must be an ordinary texture map that's an image made with
 * the camera on "the other side" of the flat mirror.
 *
 * In the case of Entropy, we can also use this for ray tracing,
 * which just requires that envname=="reflection", envspace=="current",
 * and envrad==0.
 *
 * Warning -  the environment call itself takes derivatives, causing
 * trouble if called inside a loop or varying conditional!  Be cautious.
 */
color meEnvironment ( string envname;  varying vector R;  
                    string envspace;  uniform float envrad;
                    float blur, samples, Kr;
                    uniform string filter;
            uniform float lerp;)
{
    
#if SLIM_SHADERTYPEID == SLIM_TYPEID_light
    extern point Ps;
    point Q = Ps;
#else    
    extern point P;
    point Q = P;
#endif

    color C = 0;
    if (envspace == "NDC") {
        /* envspace "NDC" signifies the special case of a flat refl map */
        point Pndc = transform ("NDC", Q);
        C = color texture (envname, xcomp(Pndc), ycomp(Pndc), "blur", blur);
    } else {
        vector Rsp;
        if (envspace != "" && envname != "reflection") {
             Rsp = normalize (vtransform (envspace, R));
             if (envrad != 0) {
                 /* Transform to the space of the environment map */
                 point Psp = transform (envspace, Q);
                 uniform float r2 = envrad * envrad;
                 /* Clamp the position to be *inside* the environment sphere */
                 if ((vector Psp).(vector Psp) > r2)
                     Psp = point (envrad * normalize (vector Psp));
                 float t0, t1;
                 if (raysphere (Psp, Rsp, envrad, 1.0e-4, t0, t1) > 0)
                     Rsp = vector (Psp + t0 * Rsp);
            }
        } else 
          Rsp = R;
        /*if ( Kr > 0.0001 ) {*/
            C = color environment (envname, Rsp, 
                       "blur", blur, 
                       "samples", samples,
                       "filter", filter,
                        "lerp", lerp);
        
          
     /* } */
    }
    return  C; /* Kr * */
}


#endif /* defined(REFLECTIONS_H) */

