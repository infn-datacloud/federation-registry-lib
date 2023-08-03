import { ImageBase } from "@/app/dashboard/_lib/dbTypes";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

export default function ImagesTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: ImageBase[];
}) {
  return (
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>UUID</TableCell>
          <TableCell>OS</TableCell>
          <TableCell>Distribution</TableCell>
          <TableCell>Version</TableCell>
          <TableCell>Architecture</TableCell>
          <TableCell>CUDA Support</TableCell>
          <TableCell>GPU Driver Support</TableCell>
          <TableCell>Creation time</TableCell>
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
              <TableCell>{item.os}</TableCell>
              <TableCell>{item.distribution}</TableCell>
              <TableCell>{item.version}</TableCell>
              <TableCell>{item.architecture}</TableCell>
              <TableCell>
                {item.cuda_support ? "Enabled" : "Disabled"}
              </TableCell>
              <TableCell>{item.gpu_driver ? "Enabled" : "Disabled"}</TableCell>
              <TableCell>{item.creation_time?.toISOString()}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
