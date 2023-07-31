"use client";

import { Flavor } from "@/app/dashboard/_lib/dbTypes";
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
} from "@mui/material";
import { ChangeEvent, useState } from "react";

export default function FlavorsTable({ items }: { items: Flavor[] }) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const rowsPerPageOptions = [5, 10, 25];

  return (
    <Paper>
      <TableContainer>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>UUID</TableCell>
              <TableCell>Num VCPUs</TableCell>
              <TableCell>Num GPUs</TableCell>
              <TableCell>RAM size (MB)</TableCell>
              <TableCell>Disk size (GB)</TableCell>
              <TableCell>Infiniband support</TableCell>
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
                  <TableCell>{item.num_vcpus}</TableCell>
                  <TableCell>{item.num_gpus}</TableCell>
                  <TableCell>{item.ram}</TableCell>
                  <TableCell>{item.disk}</TableCell>
                  <TableCell>
                    {item.infiniband_support ? "Enabled" : "Disabled"}
                  </TableCell>
                  <TableCell>{item.gpu_model}</TableCell>
                  <TableCell>{item.gpu_vendor}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={rowsPerPageOptions}
        component="div"
        count={items.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
