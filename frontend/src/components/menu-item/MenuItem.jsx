import React from "react";
import "./MenuItem.scss";
const MenuItem = ({ source, name, isSelected }) => {
  return (
    <div className={"menu-item-container " + (isSelected ? " selected" : "")}>
      <img className="menu-item-icon" src={source} alt={name} /> {name}
    </div>
  );
};
export default MenuItem;
