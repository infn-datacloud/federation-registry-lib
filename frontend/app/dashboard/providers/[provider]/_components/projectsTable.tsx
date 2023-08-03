import { ProjectBase } from "@/app/dashboard/_lib/dbTypes";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";

export default function ProjectsTable({
  items,
  page,
  rowsPerPage,
}: {
  page: number;
  rowsPerPage: number;
  items: ProjectBase[];
}) {
  return (
    <Table sx={{ minWidth: 650 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>UUID</TableCell>
          <TableCell>Public Net</TableCell>
          <TableCell>Private Net</TableCell>
          <TableCell>Private Net Proxy Host</TableCell>
          <TableCell>Private Net Proxy User</TableCell>
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
              <TableCell>{item.public_network_name}</TableCell>
              <TableCell>{item.private_network_name}</TableCell>
              <TableCell>{item.private_network_proxy_host}</TableCell>
              <TableCell>{item.private_network_proxy_user}</TableCell>
            </TableRow>
          ))}
      </TableBody>
    </Table>
  );
}
