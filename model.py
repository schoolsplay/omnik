from SQLiteWrapper import DBW

def make_db(dbpath):
    #print "Creating user sqlite tables: %s " % dbpath
    DBU = DBW(dbpath)

    DBU.define_table('minutes', [('id', 'integer', ['PRIMARY KEY']),
                                 ('InvID', 'text'),
                                  ('stamp', 'timestamp'),
                                  ('ETotal', 'real'),
                                  ('EToday', 'real'),
                                  ('Temp', 'real'),
                                  ('HTotal', 'integer'),
                                  ('VPV1', 'real'),
                                  ('VPV2', 'real'),
                                  ('VPV3', 'real'),
                                  ('IPV1', 'real'),
                                  ('IPV2', 'real'),
                                  ('IPV3', 'real'),
                                 ('VAC1', 'real'),
                                 ('VAC2', 'real'),
                                 ('VAC3', 'real'),
                                  ('IAC1', 'real'),
                                  ('IAC2', 'real'),
                                  ('IAC3', 'real'),
                                  ('FAC1', 'real'),
                                  ('FAC2', 'real'),
                                  ('FAC3', 'real'),
                                  ('PAC1', 'real'),
                                  ('PAC2', 'real'),
                                  ('PAC3', 'real')]
                     )
