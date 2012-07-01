#ifndef ME_MANIFOLD_H
#define ME_MANIFOLD_H
#include "me_util.h"
/*-----------------------------------------------------------*/
/*        */
/*-----------------------------------------------------------*/

void me_ST (
  			  uniform float angle;
  			  uniform float repeatS; uniform float repeatT;
  			  uniform float offsetS; uniform float offsetT;
  			  uniform float flipS;   uniform float flipT;
  			  output point Q;
  			  output vector dQu;
  			  output vector dQv;
  			  )
{
    extern float s, t, du, dv;

    setxcomp(Q, repeatS * s + offsetS);
    setycomp(Q, repeatT * t + offsetT);
    setzcomp(Q, 0);

    if ( angle != 0 )
      Q = rotate(Q, radians(angle), point(0,0,0), point(0,0,1)); 

    dQu = vector Du(Q)*du;
    dQv = vector Dv(Q)*dv;
    
    if ( flipS == 1 )
      setxcomp( Q, 1 - xcomp(Q) );
    if ( flipT == 1 )
      setycomp( Q, 1 - ycomp(Q) );
   
}
  
/*-----------------------------------------------------------*/
/*        */
/*-----------------------------------------------------------*/

void me_planar (
  			  uniform string coord;
  			  uniform float xper;
  			  uniform float yper;
  			  uniform float stick;
  			  output point Q;
  			  output vector dQu;
  			  output vector dQv;
  			  )
{
          point __Pref;
  		    extern point P;
      		extern normal N;
      		
      		extern float s, t, du, dv;
      		extern vector dPdu, dPdv;
      		
      		float x, y, xloc, yloc, z;
      		
      		uniform string sys = ( coord != "" ) ? coord : "world";
      			
      	  Q = (stick == 0)? transform (sys, P) : transform (sys, __Pref);
	        normal Nt = ntransform(sys, normalize(N));
	        
	        x = xcomp(Q);
	        y = ycomp(Q);
	        z = zcomp(Q);
	        
	        x += 0.5;
	        y += 0.5;
	        
	        x = 1 - x;
	        y = 1 - y;
	        
	        xloc = (xper == 0) ? x : mod( x, 1.0 );
	        yloc = (yper == 0) ? y : mod( y, 1.0 );
	        
	        setxcomp(Q, xloc );
  		    setycomp(Q, yloc );
  		    setzcomp(Q, z);

  		    dQu = vector Du(Q)*du;
  		    dQv = vector Dv(Q)*dv;	
   
}
  		
#endif
