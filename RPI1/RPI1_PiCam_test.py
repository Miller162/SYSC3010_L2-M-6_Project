""""Raspberry Pi Camera test script

This script tests that all necessary libraries to properly utilize the Pi Camera are able to be imported successfully.
It will then run a test case that causes the camera to take a picture and then use the image processing library to calculate the average relative lumenance.
This test case is outlined further in the test function docstring

This file can be imported as a module with the following functions:

    *PiCam_test - this function performs the afformentioned tests on the Pi Camera setup and implementation
"""

#TESTING import statements
try:
    import picamera
    #from picamera import PiCamera

except ImportError:
    print("PiCamera module could not be imported")

else:
    print("PiCamera module imported succesfully")
#END try-except

try:
    from PIL import Image

except ImportError:
    print("PIL module could not be imported")

else:
    print("PIL module imported successfully")

#END try-except

#TESTING PiCamera
def PiCam_test():
    """A function that runs various tests on the initiialization and implementation of the external Raspberry Pi Camera

    This function tests the Pi Camera initialization, and runs a scrip that causes it to capture an image and save it to the designated location.
    It then tests the image processing library by causing it to load that image and calculate the average relative lumenance of the image.
    Both of these tests can produce multiple different kinds of errors, most of which will be captured and properly identified by this test case.
    """
    #TESTING PiCam
    try:
        WIDTH = 64 #width for picture capture
        HEIGHT = 64 #height for picture capture
        #PiCamera setup:
        camera = picamera.PiCamera() #defining the PiCamera object
        camera.resolution = (WIDTH, HEIGHT) #set resolution (keep as small as possible to avoid lengthy calculations in the future)
        camera.capture('/home/pi/Desktop/image.jpg') #camera take picture and save to directory
        camera.close()#close the camera
    except FileNotFoundError:
        print ("Pi Camera could not save image")
    except picamera.exc.PiCameraRuntimeError:
        print ("Invalid Pi Camera operation performed during runtime")
    except picamera.exc.PiCameraClosed:
        print ("Method called on closed Pi Camera instance")
    else:
        print ("PiCamera test program has run successfully \n")
    #END try-except

    #TESTING PIL
    try:
        img = Image.open("/home/pi/Desktop/image.jpg") #opens image from location saved by the PiCamera
        luma=0 #sum of the luma of each pixels
        pixels = img.width*img.height #number of pixels in the picture

        if (pixels != WIDTH*HEIGHT): #if the expected number of pixels match the actual (same as comparing expected height and width of the image
            print("Expected width and height do not match actual")
        #END if

        for x in range(img.width): #for pixel in width
            for y in range(img.height): #for pixel in height
                (r, g, b) = img.getpixel((x,y))#get colour touple
                luma += (0.2126*r + 0.7152*g + 0.0722*b) #calculate luma of RGB data, then add to total
            #END for
        #END for
        img.close()#ensure to properly close the image
    except FileNotFoundError:
        print ("Could not find image to be opened")
    except IndexError:
        print ("Attempting to access pixels out of range")
    else:
        print("The average luma is: %d" % (luma/pixels))
        print("PIL test program has run successfully \n")
        
    #END try-except
#END PiCam_test

#PiCam_test() #for use when run as an individual file. commented out when in use as an importable library in main test file
