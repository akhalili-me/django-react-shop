export const addSingleParamToUrl = (setParams, name, value) => {
  setParams((pervParams) => {
    const allParams = new URLSearchParams(pervParams);

    if (allParams.has(name)) {
      allParams.set(name, value);
    } else {
      allParams.append(name, value);
    }

    return allParams;
  });
};

export const removeParamFromUrl = (setParams, name) => {
  setParams((pervParams) => {
    const allParams = new URLSearchParams(pervParams);

    if (allParams.has(name)) {
      allParams.delete(name);
    }

    return allParams;
  });
};

export const addArrayOfParamsToUrl = (setParams, params) => {
  setParams((pervParams) => {
    const allParams = new URLSearchParams(pervParams);

    params.forEach((p) => {
      if (allParams.has(p.name)) {
        allParams.set(p.name, p.value);
      } else {
        allParams.append(p.name, p.value);
      }
    });

    return allParams;
  });
};
