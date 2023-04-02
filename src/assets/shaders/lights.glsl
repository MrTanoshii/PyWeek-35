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
    /*
    Checks if two segments intersect
    vec2 first:     x, y of the first end of the first segment
    vec2 second:    x, y of the second end of the first segment
    vec2 third:     x, y of the first end of the second segment
    vec2 fourth:    x, y of the second end of the second segment

    return bool:    true if segments intersect, false if not

    to get familiar with what's going on here, you can read the following article on wikipedia:
    https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line_segment
    */

    vec3 r = vec3(second - first, 0.0);     // the same as (x2 - x1, y2 - y1) in the article
    vec3 s = vec3(fourth - third, 0.0);     // the same as (x4 - x3, y4 - y3) in the article
    vec3 first_third = vec3(third - first, 0.0);    // the same as (x3 - x1, y3 - y1) in the article

    // these three vectors are three-dimensional, because I decided to find determinant using cross-product
    // of two two-dimensional vectors

    float t_numerator = cross(first_third, s).z;    // numerator of t from the article
    float u_numerator = cross(first_third, r).z;    // numerator of u from the article
    float denominator = cross(r, s).z;      // denominator from the article (t and u have the same denominator)

    if (abs(denominator) <= 1e-8)       // if determinant is zero (or approximately equal to), then
        return false;                   // the segments are parallel therefore do not intersect

    //  then we should test if t and u are in the interval [0, 1], if they are then segments intersecting
    //  but division is time-consuming operation, doing some math, we can avoid division
    //  that is what's going on in the lines below

    //  if both numerator and denominator are positive
    if (0.0 <= t_numerator && t_numerator <= denominator && 0.0 <= u_numerator && u_numerator <= denominator)
        return true;
    //  if both numerator and denominator are negative
    else if (denominator <= t_numerator && t_numerator <= 0.0 && denominator <= u_numerator && u_numerator <= 0.0)
        return true;
    else
        return false;
}


bool segmentRectangleIntersection(vec4 segment, vec4 rectangle)
{
    /*
    Checks if given segment intersects given rectangle
    vec4 segment:   x, y of the first end of the segment and x, y of the second end of the segment
    vec4 rectangle  x, y of the top left vertex of the rectangle and x, y of the bottom right vertex

    return bool:    true if a segment intersects rectangle else false

    if a line intersects a rectangle, then it intersects at least one of it's diagonal,
    hence instead of checking four sides, we can check for intersection only diagonals
    the game draws obstacles after calculating the lights, hence in the end we obtain a nice picture
    */
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
    /*
    Calculates how much light is in given point
    vec3 light:         x, y, radius of a light
    vec2 pixelPosition: x, y of a pixel that we are checking

    return float:       number in interval [0, 1] that tells us how much light in the pixel
    */
    float _distance = length(light.xy - pixelPosition);

    vec4 segment = vec4(light.xy, pixelPosition);

    // Check every rectangle (obstacle) on a game plane
    for (int i = 0; i < obstaclesCount; ++i)
        if (segmentRectangleIntersection(segment, obstacles[i].xyzw))
            return 0.0;

    return 1.0 - smoothstep(0.0, light.z, _distance / 2);
}


void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    vec4 blackColor = vec4(0.f, 0.f, 0.f, TRANSPARENCY);
    vec4 preFragColor = blackColor;

    for (int i = 0; i < lightCount; ++i)
    {
        float lightAmount = computeLight(lightSources[i].xyz, fragCoord);
        vec4 color = mix(blackColor, LIGHT_COLOR, lightAmount);     // mix obtained light amount with light color
        preFragColor = mix(preFragColor, color, lightAmount);       // mix obtained color with color of texture
    }

    fragColor = preFragColor;
}
