# PyPortScan_PerIface

Takes either 1 argument being a host/IP and will scan for ports specified in script, or by default checks all interfaces, if the interface starts with 169 or 127, it will exclude it from the scan. Otherwise, it will calculate the full range from the subnet mask, create a list and scan through each IP in the subnet on the specified ports in the script.
