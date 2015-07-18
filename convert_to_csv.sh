#!/bin/bash
while getopts ":i:" opt; do
    case $opt in
        i)
            DBNAME=$OPTARG|cut -d'.' -f1
            CVSNAME=".cvs"
            sqlite3 -header -csv $OPTARG "SELECT spaceObject.name,
            spaceObject.id,
            spaceObject.mass,
            spaceObject.u,
            spaceObject.dragArea,
            spaceObject.reflectingArea,
            initState.date,
            initState.semiMajorAxis,
            initState.eccentricity,
            initState.inclination,
            initState.rAAN,
            initState.argOfPerigee,
            initState.meanAnomaly,
            finalState.date,
            finalState.timediff
            FROM initState, spaceObject, finalState Where finalState.spaceObjectId=spaceObject.id and initState.id = spaceObject.id;"
            ;;
        \?)
            echo "Invalid option -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;
    esac
done
