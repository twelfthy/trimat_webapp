import torch
from PIL import Image, ImageDraw, ImageFont
# creates a prediction
def labels_output(x):
    if x == 1:
        return "background"
    elif x == 2:
        return "L5"
    elif x == 3:
        return "L4"
    elif x == 4:
        return "L3"
    elif x == 5:
        return "L2"
    elif x == 6:
        return "L1"
    elif x == 7:
        return "T1"
    elif x == 8:
        return "T2"
    elif x == 9:
        return "T3"
    elif x == 10:
        return "T4"
    elif x == 11:
        return "T5"
    elif x == 12:
        return "T5"
    elif x == 13:
        return "T6"
    elif x == 14:
        return "T7"
    elif x == 15:
        return "T8"
    elif x == 16:
        return "T9"
    elif x == 17:
        return "T10"
    elif x == 18:
        return "T11"
    else:
        return "T12"

def create_prediction(device, model, img, bboxes_imageDir, treshold):
    with torch.no_grad():
        # prediction = model([img])
        prediction = model([img.to(device)])
    print(prediction)
    # create an image from our prediction:
    for i in range(len(prediction[0]['scores'])):
        print("confidence score: ", round(prediction[0]['scores'][i].item(),3), "detected: ",
               labels_output(prediction[0]['labels'][i].item()))
    
    image = Image.fromarray(img.mul(255).permute(1, 2, 0).byte().numpy()).convert('RGB')
    # print("image: ", image)
    # mask = Image.fromarray(prediction[0]['masks'][0, 0].mul(255).byte().cpu().numpy()).convert('RGB')

    bboxes_image = image.copy()
    # draw the confidence scores:
    

    print("number of objects detected: ",len(prediction[0]['boxes']), " \n")
    # draw the boxes and confidence scores:
    for i in range(len(prediction[0]['boxes'])):
        if prediction[0]['scores'][i].item() > treshold:
            bb_coordinates = [(prediction[0]['boxes'][i][0].item(), prediction[0]['boxes'][i][1].item()),
                               (prediction[0]['boxes'][i][2].item(), prediction[0]['boxes'][i][3].item())]
            rect_drawing = ImageDraw.Draw(bboxes_image)
            rect_drawing.rectangle(bb_coordinates, fill = None, outline = "red")
            text_position = (prediction[0]['boxes'][i][0].item(), prediction[0]['boxes'][i][1].item())
            text = str(round(prediction[0]['scores'][i].item(), 3)) + " " + labels_output(prediction[0]['labels'][i].item())
            # font = ImageFont.load_default()
            font = ImageFont.truetype('/home/ogianoli/Code/eos-landmark-detection/Fruit_tuto/Arial.ttf', size=40)
            text_color = 'black'
            draw = ImageDraw.Draw(bboxes_image)
            draw.text(text_position, text, font=font, fill=text_color)

    # mask.save(maskSaveDir)
    # image.save(imgSaveDir)
    # bboxes_image.save(bboxes_imageDir)
    return bboxes_image

def three_in_1(img1, img2, img3, bboxes_imageDir, size1, size2, size3):
    width = size1[0]+size2[0]+size3[0] #img1.size()[1] + img2.size()[1] +img3.size()[1]
    height = max(size1[1], size2[1], size3[1])
    result_image = Image.new("RGB", (width, height))

    # Paste the input images onto the output image side by side
    result_image.paste(img1, (0,0))
    result_image.paste(img2, (size1[0], 0))
    result_image.paste(img3, (size1[0]+size2[0], 0))

    # Save the output image to a file
    result_image.save(bboxes_imageDir + '3in1' + '.png')
    # return result_image