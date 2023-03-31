#define N 500
#define MAX_SOURCES 128
#define MAX_OBSTACLES 256
#define TRANSPARENCY 0.8f
#define LIGHT_COLOR vec4(75.f, 83.f, 32.f, (1.f - TRANSPARENCY) * 255.f) / 255.f


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

    vec4 segment = vec4(light.xy, pixelPosition);


    for (int i = 0; i < obstaclesCount; ++i)
        if (segmentRectangleIntersection(segment, obstacles[i].xyzw))
            return 0;

    return 1.0 - smoothstep(0.0, light.z, _distance / 2);
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec4 blackColor = vec4(0.f, 0.f, 0.f, TRANSPARENCY);
    vec4 preFragColor = blackColor;

    for (int i = 0; i < lightCount; ++i)
    {
        float lightAmount = computeLight(lightSources[i].xyz, fragCoord);
        vec4 color = mix(blackColor, LIGHT_COLOR, lightAmount);
        preFragColor = mix(preFragColor, color, lightAmount);
    }

    fragColor = preFragColor;
}
