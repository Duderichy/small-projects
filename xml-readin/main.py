import xml.etree.ElementTree as ET

class activity:
    def __init__(self, root):
        pass

class activity_search:
    def __init__(self, filepath='example.xml'):
        tree = ET.parse(filepath)
        root = tree.getroot()
        self.genders = {}
        self.ages = {}
        self.activities = {}
        for child in root:
            # child.tag == "activity"
            activity = child.attrib["value"]
            self.activities[activity] = child
            gender = child.attrib["gender"]
            if gender not in self.genders:
                self.genders[gender] = {}
            self.genders[gender][activity] = child
            # iterate over the age subgroups
            for age_sub in child:
                age_class = age_sub.tag
                age_val = age_sub.attrib["value"]
                # if the age_class isn't already in ages, add it
                if age_class not in self.ages:
                    #print(age_class)
                    self.ages[age_class] = {}
                #print(age_val)
                # if the age_val isn't already in the age_class, add it
                if age_val not in self.ages[age_class]:
                    self.ages[age_class][age_val] = set()
                self.ages[age_class][age_val].add(child)
                #print(self.ages[age_class][age_val])
        print("genders", self.genders)
        print("ages", self.ages)
        print("activities", self.activities)

    def retrieve(self, activity_name):
        ret = set()
        if activity_name in self.activities:
            activity = self.activities[activity_name]
            activity_gender = activity.attrib["gender"]
            #print(activity_gender)
            # check all the age subs
            # top vs. bottom level, most to least specific
            for age_sub in activity:
                age_val = age_sub.attrib["value"]
                age_tag = age_sub.tag
                if age_val in self.ages[age_tag]:
                    #print("age_val", age_val)
                    #print("age_tag", age_tag)
                    for match in self.ages[age_tag][age_val]:
                        #print(self.ages[age_tag][age_val])
                        #print("match", match)
                        #print(match.attrib)
                        # check against gender
                        if match.attrib["gender"] == activity_gender:
                            ret.add(match.attrib["value"])
            print(ret)
            #for thing in ret:
            #    print(thing.attrib, end = "")
            return ret
        else:
            return None   

if __name__=="__main__":
    activities = activity_search()
    activities.retrieve("weightlifting")
    activities.retrieve("jazzercise")
