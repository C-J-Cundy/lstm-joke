#Small script to convert the raw json files into more palatable
#csv files, whilst stripping out most of the uneeded stuff
import json

infile = "all-jokes-raw.txt"
outfile_verbose = "csv-jokes" #All the posts
outfile_short = "60-short-jokes" #Containing just the jokes, for short jokes
joke_len = 80 #Jokes that are up to this long go to the short file

r = open(infile,'r')
f = open(outfile_verbose, 'w') #Verbose csv file
g = open(outfile_short, 'w')

with open(infile, 'r') as r, open(outfile_verbose, 'w') as f, \
     open(outfile_short, 'w') as g:


    f.write("title, selftext, ups, downs\n")
    line_no_list = [0] #list of where the data contained ill-formed json
    for line_no, line in enumerate(r):
        if line[0] != '{':
            line = line[15:] #Get rid of filename prepended to string 
        try:
            json_line = json.loads(line)
        except ValueError:
            line_no_list.append(line_no) #Keep a record of where failed to read
            continue

        # Now don't get jokes without relevant metadata
        if ('title' not in json_line.keys() 
            or 'selftext' not in json_line.keys()
            or 'ups' not in json_line.keys()
            or 'downs' not in json_line.keys()):
            line_no_list.append(line_no)
            continue
    
        else:
            title    = json_line['title']
            selftext = json_line['selftext']
            ups      = json_line['ups']
            downs    = json_line['downs']

    #Don't fetch jokes where the body is removed or deleted
        if (selftext == '[deleted]' or selftext == '[removed]'
            or title == '[deleted]' or selftext == '[removed]'):
            continue


    #Quick-and-dirty csv: use pipe-encoding
        tmp_string = (title.encode('ascii', 'ignore') + '|'
                      + selftext.encode('ascii', 'ignore') + '|'
                      + str(ups) + '|'
                      + str(downs) + '\n')
        f.write(tmp_string)

        #Make a set of jokes with shorter 
        if (len(title) + len(selftext)) < joke_len:
            g.write((title.encode('ascii', 'ignore') + ' '
                     + selftext.encode('ascii', 'ignore').replace('\n','')
                     + '\n'))
