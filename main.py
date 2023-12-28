import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from plyer import notification 

cap = cv2.VideoCapture(0)
detector = FaceMeshDetector(maxFaces=1)
notification_shown = False

while True:
    sucess, img = cap.read()
    img = cv2.flip(img, 1)
    img, faces = detector.findFaceMesh(img, draw=False)
    if faces:
        face = faces[0]
        pointLeft = face[145]
        pointRight = face[374] 
        cv2.line(img,pointLeft,pointRight,(0,200,0),3)       
        cv2.circle(img,pointLeft,5,(255,0,255),cv2.FILLED)
        cv2.circle(img,pointRight,5,(255,0,255),cv2.FILLED)
        w,_ = detector.findDistance(pointLeft,pointRight)
        W = 6.3
        # finding the focal lenght
        # d = 60
        # f = (w*d)/W
        # print(f)        
        f = 725
        # #now calculating the distance
        d=(W*f)/w
        print(d)
        
        if d < 36:
            if not notification_shown:            
                notification_text = "You are too close to the screen!"
                notification_title = "Distance Alert"
                notification.notify(title=notification_title,message=notification_text,app_name="Face Distance Calculator",)
                notification_shown = True
                
        else:
            if notification_shown:
                notification.notify(
                    title="",
                    message="",
                    app_name="Face Distance Calculator",)
                notification_shown = False
        
        cvzone.putTextRect(img,f'Depth: {int(d)}cm',(face[10][0]-100, face[10][1]-50),scale = 2)
        
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()