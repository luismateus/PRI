from createIndex import partyGrouping

def most_mentioned_entity_in_party(partyGroup):
    print('\n##### Most mentioned entities #####')
    for k in partyGroup:
        sorting = sorted(partyGroup[k].items(), key=lambda kv: kv[1])
        sorting.reverse()
        print('Most mentioned Entity in %s is %s with %d counts' % (k, sorting[0][0], sorting[0][1]))

def most_mentioned_entity_global(partyGroup):
    print('\n##### Most mentioned Entity by all parties #####')
    mentioned = dict()
    for k in partyGroup:
        sorting = sorted(partyGroup[k].items(), key=lambda kv: kv[1])
        sorting.reverse()
        for el in sorting:
            if el[0] not in mentioned:
                mentioned[el[0]] = el[1]
            else:
                mentioned[el[0]] += el[1]
    sortin = sorted(mentioned.items(), key=lambda kv: kv[1])
    sortin.reverse()
    print('Most mentioned Entity is %s with %d counts' % (sortin[0][0], sortin[0][1]))

def most_mentioned_party(partyGroup):
    print('\n##### Most mentioned Party #####')
    mentioned = dict()
    partyList = []
    for party in partyGroup:
        partyList.append(party)
    for k in partyGroup:
        sorting = sorted(partyGroup[k].items(), key=lambda kv: kv[1])
        sorting.reverse()
        for el in sorting:
            if el[0] in partyGroup:
                if el[0] not in mentioned:
                    mentioned[el[0]] = el[1]
                else:
                    mentioned[el[0]] += el[1]
    sortin = sorted(mentioned.items(), key = lambda kv: kv[1])
    sortin.reverse()
    print('Most mentioned party is %s with %d counts' % (sortin[0][0], sortin[0][1]))

def party_mentioning_other_parties(partyGroup):
    print('\n##### Most mentioned party by other parties #####')
    mentioned = dict()
    partyList = []
    for party in partyGroup:
        partyList.append(party)
    for k in partyGroup:
        sorting = sorted(partyGroup[k].items(), key=lambda kv: kv[1])
        sorting.reverse()
        for el in sorting:
            if el[0] in partyGroup and el[0] != k:
                if k not in mentioned:
                    mentioned[k] = 0
                mentioned[k] += el[1]
    for element in mentioned:
        print('Party %s mentioned other parties %d times' % (element, mentioned[element]))

most_mentioned_entity_in_party(partyGrouping)
most_mentioned_entity_global(partyGrouping)
most_mentioned_party(partyGrouping)
party_mentioning_other_parties(partyGrouping)
