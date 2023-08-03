import { ServiceBase } from "@/app/dashboard/_lib/dbTypes";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

export default function ServicesTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: ServiceBase[];
}) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          <TableCell>Endpoint</TableCell>
          <TableCell>Type</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {items
          .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
          .map((item, index) => (
            <TableRow key={index}>
              <TableCell component="th" scope="row">
                {item.endpoint.toString()}
              </TableCell>
              <TableCell>{item.type}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
