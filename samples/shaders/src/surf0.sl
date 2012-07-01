/* Generated by meShaderEd */

#define SURFACE_SHADER surf0
surface surf0 (
)
{
color psTrace_out = color(0.000,0.000,0.000);
color surf0_Oi = color(1.000,1.000,1.000);
	
	  normal psTrace_Nf;
 		normal psTrace_Nc;
	
 		psTrace_Nf = faceforward(normalize(N), I);
    psTrace_Nc = transform("camera", (psTrace_Nf + point "camera" (0,0,0)));
    psTrace_Nc = normalize(psTrace_Nc);
		    
    setcomp(psTrace_out, 0, clamp((0.5 - xcomp(psTrace_Nc) / 2), 0, 1));
    setcomp(psTrace_out, 1, clamp((0.5 + ycomp(psTrace_Nc) / 2), 0, 1));
    setcomp(psTrace_out, 2, clamp(abs(zcomp(psTrace_Nc)), 0, 1));	
  
	  Ci = psTrace_out * surf0_Oi; 
	  Oi = surf0_Oi;
	
}
