#!/usr/bin/python3

# Hiyeon Kim, 118654
# Lars Meyer, 114719

SUN_DIAMETER = 1392000.0 * 0.000001 * 0.05 # downscale sun geometry relative to planet sizes

MERCURY_DIAMETER = 4878.0 * 0.000001 # in km
MERCURY_ORBIT_RADIUS = 58000000.0 * 0.000000002 # in km
MERCURY_ORBIT_INCLINATION = 7.0 * 3.0 # in degrees
MERCURY_ORBIT_DURATION = 87.97 # in days
MERCURY_ROTATION_INCLINATION = 0.0 # in degrees
MERCURY_ROTATION_DURATION = 58.65 # in days

VENUS_DIAMETER = 12104.0 * 0.000001 # in km
VENUS_ORBIT_RADIUS = 108200000.0 * 0.000000002 # in km
VENUS_ORBIT_INCLINATION = 3.4 # in degrees
VENUS_ORBIT_DURATION = 224.7 # in days
VENUS_ROTATION_INCLINATION = 3.0 # in degrees
VENUS_ROTATION_DURATION = 243.02 # in days

EARTH_DIAMETER = 12756.0 * 0.000001 # in km
EARTH_ORBIT_RADIUS = 149600000.0 * 0.000000002 # in km
EARTH_ORBIT_INCLINATION = 0.0 # in degrees
EARTH_ORBIT_DURATION = 365.26 # in days
EARTH_ROTATION_INCLINATION = 23.4 # in degrees
EARTH_ROTATION_DURATION = 1.0 # in days

EARTH_MOON_DIAMETER = 3476.0 * 0.000001 # in km
EARTH_MOON_ORBIT_RADIUS = 405500.0 * 0.000000002 * 30.0 # in km
EARTH_MOON_ORBIT_INCLINATION = 0.0 # in degrees
EARTH_MOON_ORBIT_DURATION = 27.32 # in days
EARTH_MOON_ROTATION_INCLINATION = 6.6 # in degrees
EARTH_MOON_ROTATION_DURATION = 0.0 # in days

MARS_DIAMETER = 6787.0 * 0.000001 # in km
MARS_ORBIT_RADIUS = 227900000.0 * 0.000000002 # in km
MARS_ORBIT_INCLINATION = 1.8 # in degrees
MARS_ORBIT_DURATION = 686.98 # in days
MARS_ROTATION_INCLINATION = 23.98 # in degrees
MARS_ROTATION_DURATION = 24.62/24.0 # in days

JUPITER_DIAMETER = 142754.0 * 0.000001 # in km
JUPITER_ORBIT_RADIUS = 778300000.0 * 0.000000002 # in km
JUPITER_ORBIT_INCLINATION = 1.3 # in degrees
JUPITER_ORBIT_DURATION = 11.86*365.0 # in days
JUPITER_ROTATION_INCLINATION = 3.1 # in degrees
JUPITER_ROTATION_DURATION = 17.23/24.0 # in days

JUPITER_MOON1_DIAMETER = 3630.0 * 0.000001 # in km
JUPITER_MOON1_ORBIT_RADIUS = 421600.0 * 0.000000002 * 200.0 # in km
JUPITER_MOON1_ORBIT_INCLINATION = 0.0 # in degrees
JUPITER_MOON1_ORBIT_DURATION = 1.769 # in days
JUPITER_MOON1_ROTATION_INCLINATION = 0.0 # in degrees
JUPITER_MOON1_ROTATION_DURATION = 0.0 # in days

JUPITER_MOON2_DIAMETER = 3138.0 * 0.000001 # in km
JUPITER_MOON2_ORBIT_RADIUS = 670900.0 * 0.000000002 * 200.0 # in km
JUPITER_MOON2_ORBIT_INCLINATION = 0.0 # in degrees
JUPITER_MOON2_ORBIT_DURATION = 3.551 # in days
JUPITER_MOON2_ROTATION_INCLINATION = 0.0 # in degrees
JUPITER_MOON2_ROTATION_DURATION = 0.0 # in days

JUPITER_MOON3_DIAMETER = 5262.0 * 0.000001 # in km
JUPITER_MOON3_ORBIT_RADIUS = 1070000.0 * 0.000000002 * 200.0 # in km
JUPITER_MOON3_ORBIT_INCLINATION = 0.0 # in degrees
JUPITER_MOON3_ORBIT_DURATION = 7.155 # in days
JUPITER_MOON3_ROTATION_INCLINATION = 0.0 # in degrees
JUPITER_MOON3_ROTATION_DURATION = 0.0 # in days

SATURN_DIAMETER = 120057.0 * 0.000001 # in km
SATURN_ORBIT_RADIUS = 1427000000.0 * 0.000000002 # in km
SATURN_ORBIT_INCLINATION = 2.5 # in degrees
SATURN_ORBIT_DURATION = 29.46*365.0 # in days
SATURN_ROTATION_INCLINATION = 26.7 # in degrees
SATURN_ROTATION_DURATION = 10.53/24.0 # in days

URANUS_DIAMETER = 51177.0 * 0.000001 # in km
URANUS_ORBIT_RADIUS = 2869600000.0 * 0.000000002 # in km
URANUS_ORBIT_INCLINATION = 0.8 # in degrees
URANUS_ORBIT_DURATION = 84.01*365.0 # in days
URANUS_ROTATION_INCLINATION = 97.9 # in degrees
URANUS_ROTATION_DURATION = 17.23/24.0 # in days

NEPTUNE_DIAMETER = 49520.0 * 0.000001 # in km
NEPTUNE_ORBIT_RADIUS = 4496600000.0 * 0.000000002 # in km
NEPTUNE_ORBIT_INCLINATION = 1.8 # in degrees
NEPTUNE_ORBIT_DURATION = 164.79*365.0 # in days
NEPTUNE_ROTATION_INCLINATION = 29.6 # in degrees
NEPTUNE_ROTATION_DURATION = 16.4/24.0 # in days

SUN_TEXTURE = "data/textures/planets/Sun.jpg"
MERCURY_TEXTURE = "data/textures/planets/mercury_rgb_cyl_www.jpg"
VENUS_TEXTURE = "data/textures/planets/venus4_rgb_cyl_www.jpg"
EARTH_TEXTURE = "data/textures/planets/Earth.jpg"
EARTH_MOON_TEXTURE = "data/textures/planets/Moon.jpg"
MARS_TEXTURE = "data/textures/planets/Mars.jpg"
JUPITER_TEXTURE = "data/textures/planets/jupiter_rgb_cyl_www.jpg"
JUPITER_MOON1_TEXTURE = "data/textures/planets/io_rgb_cyl.jpg"
JUPITER_MOON2_TEXTURE = "data/textures/planets/europa2_out.jpg"
JUPITER_MOON3_TEXTURE = "data/textures/planets/ganymede.jpg"
SATURN_TEXTURE = "data/textures/planets/saturn.jpg"
URANUS_TEXTURE = "data/textures/planets/Uranus.jpg"
NEPTUNE_TEXTURE = "data/textures/planets/Neptun.jpg"
