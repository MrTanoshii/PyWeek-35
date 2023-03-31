#define N 500
#define MAX_SOURCES 128
#define MAX_OBSTACLES 256
#define TRANSPARENCY 1


uniform vec3 lightSources[MAX_SOURCES];
uniform int lightCount;
uniform vec4 obstacles[MAX_OBSTACLES];
uniform int obstaclesCount;


bool segmentsIntersection(vec2 first, vec2 second, vec2 third, vec2 fourth)
{
    vec3 r = vec3(second - first, 0.0);
    vec3 s = vec3(fourth - third, 0.0);
    vec3 first_third = vec3(third - first, 0.0);

    float t_numerator = cross(first_third, s).z;
    float u_numerator = cross(first_third, r).z;
    float denominator = cross(r, s).z;

    if (abs(denominator) <= 1e-8)
        return false;

    if (0.0 <= t_numerator && t_numerator <= denominator && 0.0 <= u_numerator && u_numerator <= denominator)
        return true;
    else if (denominator <= t_numerator && t_numerator <= 0.0 && denominator <= u_numerator && u_numerator <= 0.0)
        return true;
    else
        return false;
}


bool segmentRectangleIntersection(vec4 segment, vec4 rectangle)
{
    vec4 firstDiagonal = rectangle;
    vec4 secondDiagonal = vec4(rectangle.z, rectangle.y, rectangle.x, rectangle.w);

    if (segmentsIntersection(firstDiagonal.xy, firstDiagonal.zw, segment.xy, segment.zw))
        return true;
    else if (segmentsIntersection(secondDiagonal.xy, secondDiagonal.zw, segment.xy, segment.zw))
        return true;
    else
        return false;
}


float computeLight(vec3 light, vec2 pixelPosition)
{
    float _distance = length(light.xy - pixelPosition);
    if (_distance > light.z)
        return 0.0;

    vec4 segment = vec4(light.xy, pixelPosition);

    for (int i = 0; i < obstaclesCount; ++i)
        if (segmentRectangleIntersection(segment, obstacles[i]))
            return 0.0;

    return 50.0;
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    float lightIntensity = 0.0;

    for (int i = 0; i < lightCount; ++i)
        lightIntensity += computeLight(lightSources[i], fragCoord);

    lightIntensity /= 255.0;

    fragColor = vec4(0.0, 0.0, 0.0, 1 - lightIntensity);
//
//    for (int i = 0; i < lightCount; ++i)
//    {
//        vec2 lightPosition = lightSources[i].xy;
//        float lightSize = lightSources[i].z;
//        float distanceToLight = length(lightPosition - fragCoord);
//
//        // Normalize the fragment coordinate from (0.0, 0.0) to (1.0, 1.0)
//        vec2 normalizedFragCoord = fragCoord / iResolution.xy;
//        vec2 normalizedLightCoord = lightPosition.xy / iResolution.xy;
//
//        // Start our mixing variable at 1.0
//        float lightAmount = 1.0;
//        for (float i = 0.0; i < N; i++)
//        {
//            // A 0.0 - 1.0 ratio between where our current pixel is, and where the light is
//            float t = i / N;
//            // Grab a coordinate between where we are and the light
//            vec2 samplePoint = mix(normalizedFragCoord, normalizedLightCoord, t);
//            // Is there something there? If so, we'll assume we are in shadow
//            float shadowAmount = terrain(samplePoint);
//            // Multiply the light amount.
//            // (Multiply in case we want to upgrade to soft shadows)
//            lightAmount *= shadowAmount;
//        }
//        if (lightAmount > maxLight)
//        {
//            // Find out how much light we have based on the distance to our light
//            lightAmount *= 1.0 - smoothstep(0.0, lightSize, distanceToLight);
//
//            // We'll alternate our display between black and whatever is in channel 1
//            vec4 blackColor = vec4(0.0, 0.0, 0.0, TRANSPARENCY);
//
//            // Our fragment color will be somewhere between black and channel 1
//            // dependent on the value of b.
//            vec4 color = mix(blackColor, texture(iChannel1, normalizedFragCoord), lightAmount);
//            maxLight = lightAmount;
//            preFragColor = mix(preFragColor, color, lightAmount);
//        }
//    }
//    fragColor = preFragColor;
}
