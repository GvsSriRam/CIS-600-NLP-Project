import React from "react";
import "./MenuItem.scss";

// MenuItem is a functional component that takes in three props: source, name, and isSelected
const MenuItem = ({ source, name, isSelected }) => {
  // The component returns a div that contains an image and the name of the menu item
  // The div's class changes based on whether the menu item is selected or not
  return (
    <div className={"menu-item-container " + (isSelected ? " selected" : "")}>
      <img className="menu-item-icon" src={source} alt={name} /> {name}
    </div>
  );
};

export default MenuItem;
