/*
utils.js

Utility functions for the application.
This file contains helper functions that are used throughout the application.
These functions are designed to be reusable and modular, making it easier to maintain and update the codebase.
The functions in this file are not specific to any particular component or feature, and can be used anywhere in the application.
*/

import { clsx } from "clsx";
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}
