import database

vchar = ' varchar(255)'
n = 'name'
sID= 'serverID'
eID = 'emoteID'
f = 'fullemote'
cID = 'chanID'
t = 'type'
rID = 'roleID'
wID = 'webhookID'
s = 'dservers'
r = 'response'

dServerCols = [n + vchar, sID + vchar]
dEmoteCols = [n + vchar, eID + vchar, f + vchar, sID + vchar]
dChanCols = [n + vchar, cID + vchar, t + vchar, sID + vchar]
dRoleCols = [n + vchar, rID + vchar, sID + vchar]
dWebHookCols = [n + vchar, wID + vchar, sID + vchar]
tComCols = [n + vchar, r + vchar + ' NOT NULL']
tQuoteCols = ['number int NOT NULL AUTO_INCREMENT, quote varchar(255) NOT NULL']

dServers = [n, sID]
dEmotes = [n , eID, f, sID]
dChannels = [n, cID, t, sID]
dRoles = [n, rID, sID]
dWebHooks = [n, wID, sID]

sqldbase = database.Database()

def runOnFirstStart():

    sqldbase.createTable(s, dServerCols, sID)
    sqldbase.createLinkedTable('demotes', dEmoteCols, eID, sID, s)
    sqldbase.createLinkedTable('dchannels', dChanCols, cID, sID, s)
    sqldbase.createLinkedTable('droles', dRoleCols, rID, sID, s)
    sqldbase.createLinkedTable('dwebhooks', dWebHookCols, wID, sID, s)

    sqldbase.createTable('tcommands', tComCols, n)
    sqldbase.createTable('tquotes', tQuoteCols, 'number')


    sqldbase.cleanup()
