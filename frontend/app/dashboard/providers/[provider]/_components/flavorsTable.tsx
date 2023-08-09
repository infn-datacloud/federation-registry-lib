import { FlavorBase } from "@/app/dashboard/_lib/dbTypes";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

export default function FlavorsTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: FlavorBase[];
}) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>UUID</TableCell>
          <TableCell>Num VCPUs</TableCell>
          <TableCell>RAM size (MB)</TableCell>
          <TableCell>Disk size (GB)</TableCell>
          <TableCell>Swap size (GB)</TableCell>
          <TableCell>Infiniband support</TableCell>
          <TableCell>Num GPUs</TableCell>
          <TableCell>GPU model</TableCell>
          <TableCell>GPU vendor</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items
          .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
          .map((item, index) => (
            <TableRow key={index}>
              <TableCell component="th" scope="row">
                {item.name}
              </TableCell>
              <TableCell>{item.uuid}</TableCell>
              <TableCell>{item.vcpus}</TableCell>
              <TableCell>{item.ram}</TableCell>
              <TableCell>{item.disk}</TableCell>
              <TableCell>{item.swap}</TableCell>
              <TableCell>
                {item.infiniband_support ? "Enabled" : "Disabled"}
              </TableCell>
              <TableCell>{item.num_gpus}</TableCell>
              <TableCell>{item.gpu_model}</TableCell>
              <TableCell>{item.gpu_vendor}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
