from ImageToSpikes import ImageToSpikes
import numpy as np
import matplotlib.pyplot as plt


# Increase neurons
#Compare to initial
spikes = []
common = []
percentages = []
prev = ImageToSpikes("2.jpg")
prev.to_spikes(7,49)
curr = ImageToSpikes("2.jpg")
for i in range(7,33):
    curr.to_spikes(i,49)
    curr_spikes = curr.get_total_number_of_spikes()
    spikes.append(curr_spikes)
    curr_common = prev.get_number_of_common_spikes(curr)
    common.append(curr_common)
    percentages.append((curr_common * 100) / curr_spikes)

plt.plot(np.arange(7,33),spikes, label = "Total spikes")
plt.plot(np.arange(7,33),common, label = "Common spikes")
plt.title("Number of spikes per per dimension and number of common spikes with the first spike output.")
plt.xlabel("Dimension of the square neuron matrix")
plt.ylabel("Spikes")
plt.legend()
plt.show()

plt.plot(np.arange(7,33),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Dimension of the square neuron matrix")
plt.ylabel("Percentage of common spikes")
plt.show()


#Compare to previous
spikes = []
common = []
percentages = []
for i in range(8,33):
    
    prev.to_spikes(i-1,49)
    curr.to_spikes(i,49)
    curr_spikes = curr.get_total_number_of_spikes()
    spikes.append(curr_spikes)
    curr_common = prev.get_number_of_common_spikes(curr)
    common.append(curr_common)
    percentages.append((curr_common * 100) / curr_spikes)

plt.plot(np.arange(8,33),spikes, label = "Total spikes")
plt.plot(np.arange(8,33),common, label = "Common spikes")
plt.title("Number of spikes per dimension and number of common spikes with the spike output of the previous dimension.")
plt.xlabel("Dimension of the square neuron matrix")
plt.ylabel("Spikes")
plt.legend()
plt.show()

plt.plot(np.arange(8,33),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Dimension of the square neuron matrix")
plt.ylabel("Percentage of common spikes")
plt.show()


#Increase runtime
#Compare to initial
spikes = []
common = []
percentages = []
prev.to_spikes(16,50)

for i in range(50,200):
    curr.to_spikes(16,i)
    curr_spikes = curr.get_total_number_of_spikes()
    spikes.append(curr_spikes)
    curr_common = prev.get_number_of_common_spikes(curr)
    common.append(curr_common)
    percentages.append((curr_common * 100) / curr_spikes)


plt.plot(np.arange(50,200),spikes, label = "Total spikes")
plt.plot(np.arange(50,200),common, label = "Common spikes")
plt.title("Number of spikes per runtime and number of common spikes with the spike output of the initial runtime.")
plt.xlabel("Runtime")
plt.ylabel("Spikes")
plt.legend()
plt.show()

plt.plot(np.arange(50,200),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Runtime")
plt.ylabel("Percentage of common spikes")
plt.show()

#Compare to previous
spikes = []
common = []
percentages = []
for i in range(10,200):
    
    prev.to_spikes(16,i-1)
    curr.to_spikes(16,i)
    curr_spikes = curr.get_total_number_of_spikes()
    spikes.append(curr_spikes)
    curr_common = prev.get_number_of_common_spikes(curr)
    common.append(curr_common)
    percentages.append((curr_common * 100) / curr_spikes)
    

plt.plot(np.arange(10,200),spikes, label = "Total spikes")
plt.plot(np.arange(10,200),common, label = "Common spikes")
plt.title("Number of spikes per runtime and number of common spikes with the spike output of the previous runtime.")
plt.xlabel("Runtime")
plt.ylabel("Spikes")
plt.legend()
plt.show()

plt.plot(np.arange(10,200),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Runtime")
plt.ylabel("Percentage of common spikes")
plt.show()



#Compare 1 to 14 other 
from PIL import Image
import glob
images = []
for file in glob.glob('images/exp1/*.jpg'):
    images.append(file)

original_image = ImageToSpikes("2.jpg")
original_image.to_spikes(16,100)

spikes = []
common = []
percentages = []

for img in images:
    img_to_compare = ImageToSpikes(img)
    img_to_compare.to_spikes(16,100)
    img_spikes = img_to_compare.get_total_number_of_spikes()
    spikes.append(img_spikes)
    img_common = original_image.get_number_of_common_spikes(img_to_compare)
    common.append(img_common)
    percentages.append((img_common * 100) / img_spikes)

plt.bar(np.arange(1,len(images) + 1),spikes, label = "Total spikes")
plt.bar(np.arange(1,len(images) + 1),common, label = "Common spikes")
plt.title("Number of spikes per picture and number of common spikes with given picture.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()

plt.plot(np.arange(1,len(images) + 1),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Images")
plt.ylabel("Percentage of common spikes")
plt.show()

#Compare 1 to N other
images = []
for file in glob.glob('images/data/*.JPG'): #images/exp1/*.jpg
    images.append(file)

original_image = ImageToSpikes("2.jpg")
original_image.to_spikes(16,200) #100

spikes = []
common = []
percentages = []

for img in images:
    img_to_compare = ImageToSpikes(img)
    img_to_compare.to_spikes(16,200) #100
    img_spikes = img_to_compare.get_total_number_of_spikes()
    spikes.append(img_spikes)
    img_common = original_image.get_number_of_common_spikes(img_to_compare)
    common.append(img_common)
    percentages.append((img_common * 100) / img_spikes)

plt.bar(np.arange(1,len(images) + 1),spikes, label = "Total spikes")
plt.bar(np.arange(1,len(images) + 1),common, label = "Common spikes")
plt.title("Number of spikes per picture and number of common spikes with given picture.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()

plt.plot(np.arange(1,len(images) + 1),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Images")
plt.ylabel("Percentage of common spikes")
plt.show()

#Compare only street to 14 other
images = []
for file in glob.glob('images/exp1/*.jpg'):
    images.append(file)

original_image = ImageToSpikes("street.jpg")
original_image.to_spikes(16,100)

spikes = []
common = []
percentages = []

for img in images:
    img_to_compare = ImageToSpikes(img)
    img_to_compare.to_spikes(16,100)
    img_spikes = img_to_compare.get_total_number_of_spikes()
    spikes.append(img_spikes)
    img_common = original_image.get_number_of_common_spikes(img_to_compare)
    common.append(img_common)
    percentages.append((img_common * 100) / img_spikes)

plt.bar(np.arange(1,len(images) + 1),spikes, label = "Total spikes")
plt.bar(np.arange(1,len(images) + 1),common, label = "Common spikes")
plt.title("Number of spikes per picture and number of common spikes with given picture.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()

plt.plot(np.arange(1,len(images) + 1),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Images")
plt.ylabel("Percentage of common spikes")
plt.show()

#Compare only street to N other
images = []
for file in glob.glob('images/data/*.JPG'): #images/exp1/*.jpg
    images.append(file)

original_image = ImageToSpikes("street.jpg")
original_image.to_spikes(16,200)

spikes = []
common = []
percentages = []

for img in images:
    img_to_compare = ImageToSpikes(img)
    img_to_compare.to_spikes(16,200) #100
    img_spikes = img_to_compare.get_total_number_of_spikes()
    spikes.append(img_spikes)
    img_common = original_image.get_number_of_common_spikes(img_to_compare)
    common.append(img_common)
    percentages.append((img_common * 100) / img_spikes)

plt.bar(np.arange(1,len(images) + 1),spikes, label = "Total spikes")
plt.bar(np.arange(1,len(images) + 1),common, label = "Common spikes")
plt.title("Number of spikes per picture and number of common spikes with given picture.")
plt.xlabel("Images")
plt.ylabel("Spikes")
plt.legend(bbox_to_anchor=(1.0, 0.2))
plt.show()

plt.plot(np.arange(1,len(images) + 1),percentages)
plt.title("Percentage of common spikes per total spikes.")
plt.xlabel("Images")
plt.ylabel("Percentage of common spikes")
plt.show()