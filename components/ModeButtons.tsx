import React from 'react'
import { useContext, useState } from "react";

const ModeButtons = () => {
  return (
    <div className="modeButtons">
      <label>
        <input type="radio" value={"value"} name={"asd"} defaultChecked={true} disabled={false}/>
        asdasd
      </label>
      <label>
        <input type="radio" value={"value"} name={"asd"} defaultChecked={true} disabled={false}/>
        asdasd
      </label>
    </div>
  );
};

export default ModeButtons;