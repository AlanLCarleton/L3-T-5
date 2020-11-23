import urllib.request
import sqlite3



def main():
    data = []
    dbconnect = sqlite3.connect("maintenanceDB.db");
    dbconnect.row_factory = sqlite3.Row;
    cursor = dbconnect.cursor();
    cursor.execute('SELECT * FROM StationStatus');
    
    #retrive data from db and put them into a list
    for row in cursor:
        data.append([row['StationLocation'],row['Bin1'],row['Bin2'],row['Bin3']])
    
    assert data[0] == [1, 20, 30, 15], "The first recond in DB should be [1, 20, 30, 15]"
    assert data[1] == [2, 50, 60, 20], "The second recond in DB should be [2, 50, 60, 20]"
    assert data[2] == [3, 40, 55, 10], "The third recond in DB should be [3, 40, 55, 10]"
    assert data[3] == [3, 65, 70, 35], "The fouth recond in DB should be [3, 65, 70, 35]"
    assert data[4] == [3, 70, 90, 50], "The fifth recond in DB should be [3, 70, 90, 50]"
    assert data[5] == [2, 50, 60, 35], "The sixth recond in DB should be [2, 50, 60, 35]"
    assert data[6] == [3, 95, 50, 60], "The seventh recond in DB should be [3, 95, 50, 60]"
    
if __name__ == '__main__':
    main()

