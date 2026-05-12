import pandas as pd

# Constants
STANDARD_PRESSURE = 1013.25 # Standard pressure in hPa

def loadData(co2File, pressureFile):
    # Load CO2 and pressure data from CSV files
    co2Data = pd.read_csv(co2File)
    pressureData = pd.read_csv(pressureFile)
    return co2Data, pressureData

def alignData(co2Data, pressureData):
    # Merge data on time, interpolate pressure for missing CO2 times
    mergedData = pd.merge_asof(
        co2Data.sort_values("time"),
        pressureData.sort_values("time"),
        on="time",
        direction="nearest"
    )
    return mergedData

def applyPressureCompensation(mergedData):
   
    mergedData["adjusted_co2_ppm"] = mergedData["raw_co2_ppm"] * (
        STANDARD_PRESSURE / mergedData["pressure_hpa"]
    )
    return mergedData

def saveAdjustedData(outputFile, adjustedData):
    
    adjustedData.to_csv(outputFile, index=False)
    print(f"Adjusted data saved to {outputFile}")

def main():
    # File paths
    co2File = "co2Data.csv"
    pressureFile = "pressureData.csv"
    outputFile = "adjustedCo2Data.csv"

    # Load data
    co2Data, pressureData = loadData(co2File, pressureFile)

    # Align and merge data
    mergedData = alignData(co2Data, pressureData)

    # Apply pressure compensation
    adjustedData = applyPressureCompensation(mergedData)

    # Save adjusted data
    saveAdjustedData(outputFile, adjustedData)

if __name__ == "__main__":
    main()
