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
        print ("PiCamera has run successfully")
    #END try-except
        
    #TESTING PIL
    try:
        img = Image.open("/home/pi/Desktop/image.jpg") #opens image from location saved by the PiCamera
        luma=0 #sum of the luma of each pixels
        pixels = img.width*img.height #number of pixels in the picture
        
        if (pixels != WIDTH*HEIGHT): #if the expected number of pixels match the actual
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
        print("PIL has run successfully")
        print("The average luma is: %d" % (luma/pixels))
    #END try-except
#END PiCam_test   

#PiCam_test()