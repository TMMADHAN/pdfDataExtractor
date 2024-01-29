import PyPDF2
import pandas as pd

# creating a pdf reader object
reader = PyPDF2.PdfReader('filename.pdf')

fullname_list = []
encounterdate_list = []
addressfacility_list = []
billingprovider_list = []
insurance_list = []
service_list = []

for i in range(len(reader.pages)):

    temp_insurance_array = []
    temp_service_array = []
    # print the text of the first page
    data = reader.pages[i].extract_text()

    # Split text by line breaks
    lines = data.split('\n')

    page_number = lines[1].split("…")[1].strip()[:3]
    # Get content from second line (index 1)
    full_name = lines[0].split('for')[1]
    if page_number[0] == '1':
        final_fullname = str(full_name.split(' ')[-1] + ' ' + full_name.split(' ')[1])
        fullname_list.append(final_fullname)

    for j, line in enumerate(lines):
        if "ADDRESSFACILITY" in line:
            addressfacility_list.append(lines[j+1].strip())  
    for line in lines:
        if 'Encounter date' in line:
            encounterdate_list.append( line.split(':')[-1].strip())
        if 'Billing provider' in line:
            billing_provider = line.split(':')[-1].strip()
            billingprovider_list.append(billing_provider )  
    if page_number[0] == '1':
        for line in lines:
            if 'INSURANCE:' in line:
                temp_insurance_array.append(line.split(':')[-1].strip())
        insurance_list.append(temp_insurance_array)
        for k, line in enumerate(lines):
            if "Service" in line:
                next_line = lines[k+1].split(' ')
                temp_service_array.append(next_line[1])
        service_list.append(temp_service_array)
    if page_number[0] == '2':
        last_insurance_list = insurance_list[-1]
        last_service_list = service_list[-1]
        for line in lines:
            if 'INSURANCE:' in line:
                temp_insurance_array.append(line.split(':')[-1].strip())
        last_insurance_list.extend(temp_insurance_array)
        for k, line in enumerate(lines):
            if "Service" in line:
                next_line = lines[k+1].split(' ')
                temp_service_array.append(next_line[1])
        last_service_list.extend(temp_service_array)

                 
    

print(len(addressfacility_list)) #
print(len(fullname_list))
print(len(insurance_list))
print(len(billingprovider_list)) #
print(len(encounterdate_list)) #
print(len(service_list))
# print(data)
df = pd.DataFrame({
    "PATIENT NAME": fullname_list,
    "ENCOUNTER DATE": encounterdate_list,
    "ADDRESSFACILITY": addressfacility_list,
    "BILLING PROVIDER": billingprovider_list,
    "INSURANCE": insurance_list,
    "SERVICE CODE": service_list,
})

# print(data)
df.to_csv("output.csv", index=False)