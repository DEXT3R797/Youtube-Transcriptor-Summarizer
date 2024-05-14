import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from transc import get_transcript
text="""No doubt war is an evil, the greatest catastrophe that befalls human beings. It brings death and destruction, disease and starvation, poverty, and ruin in its wake.
One has only to look back to the havoc that was wrought in various countries not many years ago, in order to estimate the destructive effects of war. A particularly disturbing side of modern wars is that they tend to become global so that they may engulf the entire world.
But there are people who consider war as something grand and heroic and regard it as something that brings out the best in men, but this does not alter the fact that war is a terrible, dreadful calamity.
This is especially so now that a war will now be fought with atom bombs. Some people say war is necessary. A glance at the past history will tell that war has been a recurrent phenomenon in the history of nation.
No period in world history has been the devastating effects of war. We have had wars of all types long and short. In view of this it seems futile to talk of permanent and everlasting peace or to make plans for the establishment of eternal peace.
We have had advocates of non violence and the theory of the brotherhood of man. We have had the Buddha, Christ and Mahatma Gandhi. But in spite of that, weapons have always been used, military force has always been employed, clashes of arms have always occurred; war has always been waged.
War has indeed been such a marked feature of every age and period that it has come to be regarded As part of the normal life of nations. Machiavelli, the author of the known book, The Prince, defined peace as an interval between two wars Molise, the famous German field marshal declared war to be part of God’s world order. 
Poets and prophets have dreamt of a millennium, a utopia in which war will not exist and eternal peace will reign on earth. But these dreams have not been fulfilled. After the Great War of 1914-18, it was thought that there would be no war for a long time to come and an institution called the League of Nations was founded as a safeguard against the outbreak of war.
The occurrence of another war (1939-45), however, conclusively proved that to think of an unbroken peace is to be unrealistic And that no institution or assembly can ever ensure the permanence of peace.
The League of Nations collapsed completely under the tensions and stresses created by Hitler. The United Nations Organization with all the good work that It has been doing is not proving as effective as was desired.
Large numbers of Wars, the most recent ones being the one in Vietnam, the other between India and Pakistan, or indo-china War, Iran-Iraq war or Arab Israel war, have been fought despite the UN. The fact of the matter is that fighting in a natural instinct in man.
When individuals cannot live always in peace, it is, indeed, too much to expect so many nations to live in a state of Eternal peace. Besides, there will always be wide differences of opinion between various nation, different angles of looking at matters that have international importance, radical difference in policy and ideology and these cannot be settled by mere discussions.
So resort to war becomes necessary in such circumstances. Before the outbreak of World War II, for instance, the spread of Communism in Russia created distrust and suspicion in Europe, democracy was an eyesore to Nazi Germany, British Conservatives were apprehensive of the possibility of Britain going Communist.
In short, the political ideology of one country being abhorrent to other times were certainly not conducive to the continuance of peace. Add to all this the traditional enemities between nations and international disharmony that have their roots in past history.
For example, Germany wished to avenge the humiliating terms imposed upon her at the conclusion of the war of 1914-18 and desired to smash the British Empire and establish an empire of her own. Past wounds, in fact, were not healed up and goaded it to take revenge.
A feverish arms race was going on between the hostile nations in anticipation of such an eventuality, and disarmament efforts were proving futile. The Indo-Pakistan war was fought over the Kashmir issue.
The war in Vietnam Was due to ideological differences. It also appears that if peace were to continue for a long period, people would become sick of the monotony of life and would seek war for a changed man is a highly dynamic creature and it seems that he cannot remain contented merely with works of peace-the cultivation of arts, the development of material comforts, the extension of knowledge, the means and appliances of a happy life.
He wants something thrilling and full of excitement and he fights in order to get an outlet for his accumulated energy. It must be admitted, too, that war Has its good side. It spurs men to heroism and self-sacrifice. It is an incentive to scientific research and development. War is obviously an escape from the lethargy of peace."""

def sunmmarizer(rawdoc):
    stopwords =list(STOP_WORDS)
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdoc)
    #print(doc)
    tokens = [token.text for token in doc]
    #print(tokens)
    word_feq ={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_feq.keys():
                word_feq[word.text]=1
            else:
                word_feq[word.text]+= 1

    #print(word_feq)

    max_freq =max(word_feq.values())
    #print(max_freq)

    for word in word_feq.keys():
        word_feq[word] =word_feq[word]/max_freq

    #print(word_feq)

    sent_tokens=[sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
          if word.text in word_feq.keys():
            if sent not in sent_scores.keys():
                sent_scores[sent] =word_feq[word.text]
            else:
                    sent_scores[sent]+= word_feq[word.text]   

    #print(sent_scores)                

    select_len =int(len(sent_tokens)*0.3)
    #print(select_len)

    summary = nlargest(select_len,sent_scores,key=sent_scores.get)
    #print(summary)
    final_Summary= [word.text for word in summary]
    summary=''.join(final_Summary)
    #print(summary)
    #print("Length of orginal text" ,len(text.split(' ')))
    #print("Length of summary text" ,len(summary.split(' ')))
    return summary ,doc ,len(rawdoc.split(' ')),len(summary.split(' '))
    