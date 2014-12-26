__author__ = 'mac'

import Personalization.text_analysis as ta

def load_profiles():
    default = ta.default_profile()
    cs = ta.cs_profile()
    cs_artist = ta.cs_and_artist_profile()
    profile_by_id = dict()
    profile_by_id['E4:40:E2:66:0C:EB'] = cs
    profile_by_id['BLUETOOTH2'] = cs_artist
    profile_by_id['BLUETOOTH3'] = default
    return profile_by_id

def get_profile(profiles, id):
    if id in profiles:
        return ta.default_profile()
    return profiles[id]

def example():
    model = ta.TextAnalyzer()
    # this call load the model from the directory where Personalization/text_analysis.py is saved
    model.read_model()

    default = ta.default_profile()
    cs = ta.cs_profile()
    cs_artist = ta.cs_and_artist_profile()


    profile_by_id = load_profiles()

    res = ta.get_personalized_content(model, default, 4)
    print "Content for default"
    for item in res:
        print item
        print "\n#############################\n"
    res = ta.get_personalized_content(model, cs, 4)
    print "Content for computer guy"
    for item in res:
        print item
        print "\n#############################\n"
    print len(cs)
    print len(cs_artist)
    res = ta.get_personalized_content(model, cs_artist, 4)
    print "Content for computer and artist guy"
    for item in res:
        print item
        print "\n#############################\n"

def example2():
    model = ta.TextAnalyzer()
    # this call load the model from the directory where Personalization/text_analysis.py is saved
    model.read_model()

    profiles = load_profiles()

    cs = get_profile(profiles, 'E4:40:E2:66:0C:EB')
    print cs

example2()