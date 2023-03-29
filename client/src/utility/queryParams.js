export const addNewParam = (setParams,name,value) => {
    setParams((pervParams) => {
      const allParams = new URLSearchParams(pervParams)

      if (allParams.has(name)) {
        allParams.set(name,value)
      } else {
        allParams.append(name,value)
      }

      return allParams
    })
  }