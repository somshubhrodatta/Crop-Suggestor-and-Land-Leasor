#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 16:45:08 2023

@author: somshubhrodatta
"""
import random
import sqlite3 as sql
db = sql.connect('lease.db', timeout=100000)
'''db.execute('drop table if exists user')
db.execute('drop table if exists plot_details')'''
db.execute('create table if not exists plot_details(id int primary key, size float ,state varchar(15), district varchar(15), ownerph bigint, rate float, tenantph bigint)')
db.execute('create table if not exists user( name varchar(20), phone_no bigint primary key, password varchar(8))')
db.commit()


def landreg(state, district, ownerph, size, rate):
    id = random.randint(1, 10000000)
    query = 'INSERT INTO plot_details VALUES (?, ?, ?, ?, ?, ?, NULL)'
    values = (id, size, state, district, ownerph, rate)
    db.execute(query, values)
    db.commit()


def userreg(name, phone_no, password):
    query = 'INSERT INTO user VALUES (?, ?, ?)'
    values = (name, phone_no, password)
    db.execute(query, values)
    db.commit()
    


def leaseapp(ph, landid):
    query = 'update plot_details set tenantph=? where id=?'
    values = (ph, landid)
    db.execute(query, values)
    db.commit()


def showplot(state,district):
    if(state and district):
        query='select p.id,p.size, p.rate, u.name,u.phone_no, from plot_details p left join user u on p.ownerph=u.phone_no where state=? and district=? and tenantph is NULL'
        values=(state,district)
        for row in db.execute(query,values).fetchall():
            print(row)
    else:
        for row in db.execute('select* from plot_details order by rate and tenantph is NULL').fetchall():
            print(row) 
    db.commit()

    
def showusers(phone,password):
    for row in db.execute('select* from user where phone_no=? and password=?',(phone,password)).fetchone():
        db.commit()
        return row
    db.commit()
    
    
def showph(phone):
     row=db.execute('select phone_no from user where phone_no=?',(phone,)).fetchall()
     db.commit()
     return row
def showrec(phone):
    print("Owned:")
    print("(state,district,id)")
    for row in db.execute('select state,district,id from plot_details where ownerph=?',(phone,)):
        print(row)
    print("Rented:")
    print("(state,district,id)")
    for row in db.execute('select state,district,id from plot_details where tenantph=?',(phone,)):
        print(row)
m=10  
while(m!=0):
 print("1. Login \n2. Signup\n3. Quit")
 m=int(input("Your choice: "))
 if m==2:
    p=int(input("Phone: "))
    n=(input("Name: "))
    pw=(input("Password: "))
    print
    if len(showph(p))==0:
        userreg(n,p,pw)
        print("Successful")
    else:
        print("Phone no. already used")
 elif m==1:
    p=int(input("Phone: "))
    pw=(input("Password: "))
    if showusers(p,pw)==None:
        print("Invalid credentials")
    else:
        print("1. Register a plot\n2. Rent a plot\n3.show portfolio\n0. Quit")
        c=int(input("Your choice: "))
        if c==1:
          s=input("State: ")
          d=input("District: ")
          si=float(input("Size in sq.m: "))
          r=float(input("Rate: "))
          landreg(s,d,p,si,r)
        elif c==2:
          s=input("State: ")
          d=input("District: ")
          print("(id,size,rate,owner,contact no.)")
          showplot(s,d)
          i=int(input("Enter id of the desired plot: "))
          leaseapp(p,i)
          print("The plot has been leased to you")
        elif c==3:
          showrec(p)
        elif c==0:
          break
        else:
          print("Invalid")
 elif m==0:
     break
 else:
    print("Invalid")
    

