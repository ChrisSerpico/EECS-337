import re
import sys

variations = {'Best Motion Picture - Drama': [],
'Best Motion Picture - Comedy Or Musical': [],
'Best Performance by an Actress in a Motion Picture - Drama': [],
'Best Performance by an Actor in a Motion Picture - Drama': [],
'Best Performance by an Actress in a Motion Picture - Comedy Or Musical': [],
'Best Performance by an Actor in a Motion Picture - Comedy Or Musical': [],
'Best Performance by an Actress in a Supporting Role in a Motion Picture': ['Best Supporting Actress', 'Best Supporting Actress in a Motion Picture', 'Best Supporting Actress in a Movie', 'Best Performance by Supporting Actress',
                                                                            'Best Actress in Supporting Role'],
'Best Performance by an Actor in a Supporting Role in a Motion Picture': [],
'Best Director - Motion Picture': ['Best Director', 'Best Motion Picture Director', 'Best Movie Director', 'Award for Director', 'Director Award'],
'Best Screenplay - Motion Picture': [],
'Best Motion Picture - Animated': [],
'Best Animated Feature Film': [],
'Best Foreign Language Film': [],
'Best Original Score - Motion Picture': [],
'Best Original Song - Motion Picture': [],
'Best Television Series - Drama': [],
'Best Television Series - Comedy Or Musical': [],
'Best Mini-Series Or Motion Picture Made for Television': [],
'Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television': [],
'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television': [],
'Best Performance by an Actress in a Television Series - Drama': [],
'Best Performance by an Actor in a Television Series - Drama': ['Best Actor in Television Drama', 'Best Television Drama Actor', 'Best TV Drama Actor', 'Best Actor in TV Drama Series', 'Best Actor in Television Drama Series'],
'Best Performance by an Actress in a Television Series - Comedy Or Musical': [],
'Best Performance by an Actor in a Television Series - Comedy Or Musical': [],
'Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': [],
'Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': []}

patterns1 = {'Best Motion Picture - Drama': re.compile(r''),
'Best Motion Picture - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actress in a Motion Picture - Drama': re.compile(r''),
'Best Performance by an Actor in a Motion Picture - Drama': re.compile(r''),
'Best Performance by an Actress in a Motion Picture - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actor in a Motion Picture - Comedy Or Musical': re.compile(r''),
             #Given the high number of optional segments, basically any other performance award can come up as a false positive
'Best Performance by an Actress in a Supporting Role in a Motion Picture': re.compile(r'Best (Support(ing)?|Performance|Actress)( by| in)?( an?)?( Actress| Support(ing)?)?( Actress| Role)?', re.I),
'Best Performance by an Actor in a Supporting Role in a Motion Picture': re.compile(r''),
             #This one is particularly prone to false positives, since anything can be in between the two supplied words
             #For example, someone could easily say "Best Television Series was lame.... that Director sucks!" or something along those lines, which would still be seen as matching
'Best Director - Motion Picture': re.compile(r'(Best (.)*Director)|(Award (.)*Director)|(Director (.)*Award)'),
'Best Screenplay - Motion Picture': re.compile(r''),
'Best Motion Picture - Animated': re.compile(r''),
'Best Animated Feature Film': re.compile(r''),
'Best Foreign Language Film': re.compile(r''),
'Best Original Score - Motion Picture': re.compile(r''),
'Best Original Song - Motion Picture': re.compile(r''),
'Best Television Series - Drama': re.compile(r''),
'Best Television Series - Comedy Or Musical': re.compile(r''),
'Best Mini-Series Or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actress in a Television Series - Drama': re.compile(r''),
             #This one could potentially match with pretty much any other television series award, unfortunately
             #eg Best Actor in Television Comedy, Best Actor in Television Series - Musical
'Best Performance by an Actor in a Television Series - Drama': re.compile(r'Best (Actor|Television|TV) (in|Drama)( Television| Actor| TV| Drama)', re.I),
'Best Performance by an Actress in a Television Series - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actor in a Television Series - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': re.compile(r'')}

patterns2 = {'Best Motion Picture - Drama': re.compile(r''),
'Best Motion Picture - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actress in a Motion Picture - Drama': re.compile(r''),
'Best Performance by an Actor in a Motion Picture - Drama': re.compile(r''),
'Best Performance by an Actress in a Motion Picture - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actor in a Motion Picture - Comedy Or Musical': re.compile(r''),
             # we can get rid of the false positives for this one relatively easily by simply making Actress/Supporting mandatory instead of optional
'Best Performance by an Actress in a Supporting Role in a Motion Picture': re.compile(r'Best (Support(ing)?|Performance|Actress)( by| in)?( an?)?( Actress| Support(ing)?)( Actress| Role)?', re.I),
'Best Performance by an Actor in a Supporting Role in a Motion Picture': re.compile(r''),
             # We can get rid of the false positives by being much more explicit
             # Unfortunately, this makes the expression much less flexible, meaning possible variations we didn't think of will slip through
'Best Director - Motion Picture': re.compile(r'(Best (Motion Picture |Movie )?Director)|(Award (.)*Director)|(Director Award)'),
'Best Screenplay - Motion Picture': re.compile(r''),
'Best Motion Picture - Animated': re.compile(r''),
'Best Animated Feature Film': re.compile(r''),
'Best Foreign Language Film': re.compile(r''),
'Best Original Score - Motion Picture': re.compile(r''),
'Best Original Song - Motion Picture': re.compile(r''),
'Best Television Series - Drama': re.compile(r''),
'Best Television Series - Comedy Or Musical': re.compile(r''),
'Best Mini-Series Or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actress in a Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actor in a Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actress in a Television Series - Drama': re.compile(r''),
             # We can add another term, forcing there to be 'Drama' after 'Television'
             # This gets rid of the false positive, but again, makes the expression a lot less flexible for things we didn't think of
'Best Performance by an Actor in a Television Series - Drama': re.compile(r'Best (Actor|Television|TV) (in|Drama)( Television Drama| Actor| TV| Drama)', re.I),
'Best Performance by an Actress in a Television Series - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actor in a Television Series - Comedy Or Musical': re.compile(r''),
'Best Performance by an Actress in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': re.compile(r''),
'Best Performance by an Actor in a Supporting Role in a Series, Mini-Series or Motion Picture Made for Television': re.compile(r'')}

fp = ['Best Foreign Film was the worst, that Director is terrible', 'Best Actor in Television Comedy', 'Best Actor in Television Series - Musical',
      'Best Performance by an Actor in a Motion Picture - Drama', 'Best Performance by an Actor in a Supporting Role in a Motion Picture']

# FOR QUESTION 3
# While none of the original variations stopped being matched by the new expressions, in a real situation it's almost guaranteed that the new expressions would miss out on a lot of
# variations I didn't think of at the beginning. While there would be fewer false positives, there would be more misses. This could be good if we're working with very sensitive or important data.
# For example, if we were looking through hundreds of thousands of emails for the NSA to look for incriminating messages, misses would be bad, but it would be much worse to sift through tons
# of false positives - a few emails slipping through would probably be worth finding the ones that really matter. On the other hand, if we're working with data that's more for fun or for interesting
# statistics purposes, we would probably prefer false positives. If we were looking through a bunch of tweets about some topic, say a television finale, it'd be a lot more interesting to accidentally count
# a few extra people who were positive or negative on the finale then to say a smaller proportion of people had an opinion. Generally, when we're trying to narrow text down or look for something very
# specific in text, it's a lot more important to avoid false positive. On the other hand, when we're attempting to generalize about a large body of text, it's probably more useful to avoid misses. 

def falseneg(awards):
    print "Ideally you want all of the variations to match."
    for award in awards:
        print award
        print "="*len(award)
        print "VARIATION\t\tSTATUS\t\tMATCHING SUBSTRING"
        for variation in variations[award]:
            match = re.search(patterns1[award], variation)
            if match:
                print "%s\t\tmatch\t\t%s" % (variation, match.group(0))
            else:
                print "%s\t\tno match" % variation

def falsepos(awards):
    print "Ideally, you want none of these to match. The variations are the potential false positives."
    for award in awards:
        print award
        print "="*len(award)
        print "VARIATION\t\tSTATUS\t\tMATCHING SUBSTRING"
        for s in fp:
            match = re.search(patterns2[award], s)
            if match:
                print "%s\t\tmatch\t\t%s" % (s, match.group(0))
            else:
                print "%s\t\tno match" % s

def balance(awards):
    print "Ideally you want all of the variations to match."
    for award in awards:
        print award
        print "="*len(award)
        print "VARIATION\t\tSTATUS\t\tMATCHING SUBSTRING"
        for variation in variations[award]:
            match = re.search(patterns2[award], variation)
            if match:
                print "%s\t\tmatch\t\t%s" % (variation, match.group(0))
            else:
                print "%s\t\tno match" % variation

if __name__ == '__main__':
    awards = [award for award in variations if variations[award]]
    if sys.argv[1] == 'falseneg':
        falseneg(awards)
    elif sys.argv[1] == 'falsepos':
        falsepos(awards)
    elif sys.argv[1] == 'balance':
        balance(awards)
