/* Generated by meShaderEd */

#define DISPLACEMENT_SHADER displace
displacement displace (
)
{
normal N_N = normal(0.000,0.000,0.000);
point P_P = point(0.000,0.000,0.000);
float IDbubbly_Kd = 0.200;
float IDbubbly_mult = 5.000;
float IDbubbly_Nzscale = 1.000;
float IDbubbly_bubsize = 1.000;
point IDbubbly_outP = point(0.000,0.000,0.000);
normal IDbubbly_outN = normal(0.000,0.000,0.000);

	  #ifdef SURFACE_SHADER
	  P_P = P;
	  #endif
	  #ifdef DISPLACEMENT_SHADER
	  P_P = P;
	  #endif
	  #ifdef LIGHT_SHADER
	  P_P = Ps;
	  #endif
	  #ifdef VOLUME_SHADER
	  P_P = Pv;
	  #endif
	  
	#ifdef SURFACE_SHADER
	  N_N = N;
	  #endif
	  #ifdef DISPLACEMENT_SHADER
	  N_N = N;
	  #endif
	  #ifdef LIGHT_SHADER
	  N_N = Ns;
	  #endif
	  #ifdef VOLUME_SHADER
	  N_N = Nv;
	  #endif
	
	  normal IDbubbly_Nn = normalize(N_N);
    float IDbubbly_a, IDbubbly_b, IDbubbly_c, IDbubbly_bub;
    float IDbubbly_dist, IDbubbly_shortest=10000;
    
    point IDbubbly_Po = transform( "object", P_P ) * IDbubbly_mult;
  
    /* true cell center, surrounding cell centers, noised cell center */
    point IDbubbly_trucell, IDbubbly_surrcell, IDbubbly_nzcell;
    vector IDbubbly_offset;
    
    setxcomp ( IDbubbly_trucell, floor ( xcomp ( IDbubbly_Po ) ) + .5 );
    setycomp ( IDbubbly_trucell ,floor ( ycomp ( IDbubbly_Po ) ) + .5 );
    setzcomp ( IDbubbly_trucell, floor ( zcomp ( IDbubbly_Po ) ) + .5 );
  			     
    /* what is the shortest distance to a noised cell center? */
    for ( IDbubbly_a = -1 ; IDbubbly_a <= 1 ; IDbubbly_a += 1 ) 
    {
      for ( IDbubbly_b = -1 ; IDbubbly_b <= 1 ; IDbubbly_b += 1 )
      {
        for ( IDbubbly_c = -1 ; IDbubbly_c <= 1 ; IDbubbly_c += 1 )
        {
        	IDbubbly_offset = vector ( IDbubbly_a, IDbubbly_b, IDbubbly_c );
        	IDbubbly_surrcell = IDbubbly_trucell + IDbubbly_offset;
        	IDbubbly_nzcell = IDbubbly_surrcell + ( ( vector cellnoise ( IDbubbly_surrcell ) - .5) * IDbubbly_Nzscale );
        	IDbubbly_dist = distance ( IDbubbly_Po, IDbubbly_nzcell );
        	if ( IDbubbly_dist < IDbubbly_shortest ) 
        	  IDbubbly_shortest = IDbubbly_dist;
        }
      }
    }
    IDbubbly_bub = clamp ( IDbubbly_shortest, 0, IDbubbly_bubsize ) / IDbubbly_bubsize; 
    P_P += IDbubbly_Nn * ( pow ( IDbubbly_bub, 2 ) - 1 ) * IDbubbly_Kd;
    N_N = calculatenormal ( P_P );
          
	  IDbubbly_outP = P_P; 
	  IDbubbly_outN = N_N;
	  
	  P = IDbubbly_outP; 
	  N = IDbubbly_outN;
	
}
