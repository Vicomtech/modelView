#!/bin/sh

export evapihost=`jq -r .endpoints.REMOTE[1].machine envconfig.json`
export vizapihost=`jq -r .endpoints.REMOTE[0].machine envconfig.json`
export evapiport=`jq -r .endpoints.REMOTE[1].port envconfig.json`
export vizapiport=`jq -r .endpoints.REMOTE[0].port envconfig.json`
export evapiroot=`jq -r .endpoints.REMOTE[1].root envconfig.json`
export vizapiroot=`jq -r .endpoints.REMOTE[0].root envconfig.json`

if [[ $evapiroot != "" ]]
then
  evapiroot=$evapiroot"/"
fi

if [[ $vizapiroot != "" ]]
then
  vizapiroot=$vizapiroot"/"
fi

sub=`envsubst '$evapihost,$evapiport,$evapiroot,$vizapihost,$vizapiport,$vizapiroot' < ../nginx/nginx.conf.template`

echo "$sub"