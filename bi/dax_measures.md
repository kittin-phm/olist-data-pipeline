 # DAX Measures

## Total GMV
```dax
Total GMV = SUM(vw_monthly_gmv[monthly_gmv])
```
Calculates total Gross Merchandise Value across all months.

## Avg AOV
```dax
Avg AOV = AVERAGE(vw_aov[aov])
```
Calculates average order value across all months.

## Avg Ontime Rate
```dax
Avg Ontime Rate = AVERAGE(vw_ontime_delivery[ontime_delivery_rate_pct])
```
Calculates average on-time delivery rate percentage across all months.
