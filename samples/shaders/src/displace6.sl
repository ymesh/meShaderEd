/* Generated by meShaderEd */

#define DISPLACEMENT_SHADER displace6
displacement displace6 (
float IDbubbly6_Kd = 0.200;
float IDbubbly6_mult = 5.000;
float IDbubbly6_Nzscale = 1.000;
float IDbubbly6_bubsize = 1.000;
)
{
normal N6_N = normal(0.000,0.000,0.000);
point P6_P = point(0.000,0.000,0.000);
point IDbubbly6_outP = point(0.000,0.000,0.000);
normal IDbubbly6_outN = normal(0.000,0.000,0.000);

	  #ifdef SURFACE_SHADER
	  P6_P = P;
	  #endif
	  #ifdef DISPLACEMENT_SHADER
	  P6_P = P;
	  #endif
	  #ifdef LIGHT_SHADER
	  P6_P = Ps;
	  #endif
	  #ifdef VOLUME_SHADER
	  P6_P = Pv;
	  #endif
	  
	#ifdef SURFACE_SHADER
	  N6_N = N;
	  #endif
	  #ifdef DISPLACEMENT_SHADER
	  N6_N = N;
	  #endif
	  #ifdef LIGHT_SHADER
	  N6_N = Ns;
	  #endif
	  #ifdef VOLUME_SHADER
	  N6_N = Nv;
	  #endif
	
	  normal IDbubbly6_Nn = normalize(N6_N);
    float IDbubbly6_a, IDbubbly6_b, IDbubbly6_c, IDbubbly6_bub;
    float IDbubbly6_dist, IDbubbly6_shortest=10000;
    
    point IDbubbly6_Po = transform( "object", P6_P ) * IDbubbly6_mult;
  
    /* true cell center, surrounding cell centers, noised cell center */
    point IDbubbly6_trucell, IDbubbly6_surrcell, IDbubbly6_nzcell;
    vector IDbubbly6_offset;
    
    setxcomp ( IDbubbly6_trucell, floor ( xcomp ( IDbubbly6_Po ) ) + .5 );
    setycomp ( IDbubbly6_trucell ,floor ( ycomp ( IDbubbly6_Po ) ) + .5 );
    setzcomp ( IDbubbly6_trucell, floor ( zcomp ( IDbubbly6_Po ) ) + .5 );
  			     
    /* what is the shortest distance to a noised cell center? */
    for ( IDbubbly6_a = -1 ; IDbubbly6_a <= 1 ; IDbubbly6_a += 1 ) 
    {
      for ( IDbubbly6_b = -1 ; IDbubbly6_b <= 1 ; IDbubbly6_b += 1 )
      {
        for ( IDbubbly6_c = -1 ; IDbubbly6_c <= 1 ; IDbubbly6_c += 1 )
        {
        	IDbubbly6_offset = vector ( IDbubbly6_a, IDbubbly6_b, IDbubbly6_c );
        	IDbubbly6_surrcell = IDbubbly6_trucell + IDbubbly6_offset;
        	IDbubbly6_nzcell = IDbubbly6_surrcell + ( ( vector cellnoise ( IDbubbly6_surrcell ) - .5) * IDbubbly6_Nzscale );
        	IDbubbly6_dist = distance ( IDbubbly6_Po, IDbubbly6_nzcell );
        	if ( IDbubbly6_dist < IDbubbly6_shortest ) 
        	  IDbubbly6_shortest = IDbubbly6_dist;
        }
      }
    }
    IDbubbly6_bub = clamp ( IDbubbly6_shortest, 0, IDbubbly6_bubsize ) / IDbubbly6_bubsize; 
    P6_P += IDbubbly6_Nn * ( pow ( IDbubbly6_bub, 2 ) - 1 ) * IDbubbly6_Kd;
    N6_N = calculatenormal ( P6_P );
          
	  IDbubbly6_outP = P6_P; 
	  IDbubbly6_outN = N6_N;
	  
	  P = IDbubbly6_outP; 
	  N = IDbubbly6_outN;
	
}
