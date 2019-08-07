/* Filtered versions of some functions. */
#ifndef __FILTERED_H
#define __FILTERED_H 1


float filteredstep(float edge, x, fw)
{
    return clamp((x+fw/2-edge)/fw, 0, 1);
}

#ifndef PATTERNS_H
float filteredsmoothstep(float a, b, x, fw)
{
    float value;
    
    if(abs(b-a) < fw)
        value = filteredstep((b+a)/2, x, fw);
    else
        value = smoothstep(a, b, x);
        
    return value;
}

float filteredsmoothpulse(float a, b, fuzz, x, fw)
{
    return filteredsmoothstep(a, a+fuzz, x, fw) - filteredsmoothstep(b-fuzz, b,(x), fw);
}
#endif
#endif